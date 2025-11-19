# agents.py
"""
Life Unstuck AI – Multi-agent system powered by Gemini 2.5 Flash.
Optimized to use only 2 Gemini calls per request (no 429 errors).
CrewAI is optional & used only as orchestration layer.
"""

import os
import base64
from dotenv import load_dotenv

load_dotenv()

# Optional CrewAI import
try:
    from crewai import Crew, Agent
    CREWAI_AVAILABLE = True
except:
    CREWAI_AVAILABLE = False

# Gemini imports
try:
    from google.api_core.client_options import ClientOptions
    from google.ai.generativelanguage import GenerativeServiceClient
    from google.ai.generativelanguage_v1beta.types import Part, Content
    GEMINI_AVAILABLE = True
except:
    GEMINI_AVAILABLE = False

# ENV
API_KEY = os.getenv("GEMINI_API_KEY")
TEXT_MODEL = os.getenv("TEXT_MODEL", "models/gemini-2.5-flash")
IMAGE_MODEL = os.getenv("IMAGE_MODEL", "models/gemini-flash-latest")

# Gemini client init
client = None
if GEMINI_AVAILABLE and API_KEY:
    try:
        client = GenerativeServiceClient(client_options=ClientOptions(api_key=API_KEY))
    except:
        client = None

# ----------- GEMINI CALL WRAPPER (RETRY LOGIC) -----------
def run_gemini(prompt: str, model=TEXT_MODEL):
    if not client:
        return "AI unavailable."
    
    for attempt in range(3):
        try:
            resp = client.generate_content(
                model=model,
                contents=[Content(parts=[Part(text=prompt)])]
            )
            return resp.candidates[0].content.parts[0].text.strip()
        except Exception as e:
            if "429" in str(e):
                continue
            return f"[Error: {str(e)}]"
    return "[Retry limit reached]"

# ----------- IMAGE ANALYSIS -----------
def analyze_image(image_bytes):
    try:
        b64 = base64.b64encode(image_bytes).decode()
        prompt = "Describe this image in 3–4 simple lines in friendly English."
        resp = client.generate_content(
            model=IMAGE_MODEL,
            contents=[Content(parts=[
                Part(text=prompt),
                Part(inline_data={"mime_type": "image/png", "data": b64})
            ])]
        )
        return resp.candidates[0].content.parts[0].text.strip()
    except:
        return ""

# ----------- MAIN MULTI-AGENT 2-CALL PIPELINE -----------
def run_multi_agents(category_unused, text, image_bytes=None):
    # CALL 1 → Create structured AGENT NOTE
    image_info = ""
    if image_bytes:
        image_info = analyze_image(image_bytes)

    prompt1 = f"""
You are a multi-agent coordinator.
User message: {text}

Image info (if any): {image_info}

Determine which category fits best from:
emotional, study, motivation, decision, productivity, general.

Then generate a focused agent note:
- If emotional → give supportive strategies.
- If study → give study plan + timing.
- If decision → give pros/cons + next action.
- If productivity → give momentum steps.
- If general → give common-sense steps.

Return ONLY in this format:

CATEGORY: <one word>
AGENT_NOTE: <short paragraph>
"""

    agent_output = run_gemini(prompt1)

    # CALL 2 → Final 5 steps + tip (old style output)
    prompt2 = f"""
You are a friendly polisher.

Using ONLY the agent note below, produce:

- 5 very simple, actionable steps (numbered 1–5)
- 1 helpful tip (one short line)

Rules:
- Very simple English
- Student-friendly tone
- DO NOT repeat prompt or agent note
- DO NOT output anything else

Agent info:
{agent_output}

Return in this exact format:

1) ...
2) ...
3) ...
4) ...
5) ...

Tip: ...
"""

    return run_gemini(prompt2)
