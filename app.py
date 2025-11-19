# app.py
import os
import streamlit as st
from io import BytesIO
from langdetect import detect
from dotenv import load_dotenv

load_dotenv()

from agents import run_multi_agents

# -------- INLINE SVG LOGO WITH "LUI" --------
SVG_LOGO = """
<svg width="80" height="80" viewBox="0 0 100 100"
     xmlns="http://www.w3.org/2000/svg" style="border-radius:18px;">
  <defs>
    <linearGradient id="grad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#6EA8FF"/>
      <stop offset="100%" stop-color="#3D6BFF"/>
    </linearGradient>
  </defs>
  <rect width="100" height="100" rx="22" fill="url(#grad)"/>
  <text x="50" y="58" font-size="34" text-anchor="middle"
        fill="white" font-family="Segoe UI" font-weight="bold">LUI</text>
</svg>
"""

# -------- LANGUAGE DETECTION --------
def detect_language_safe(text):
    try:
        lang = detect(text)
        if lang.startswith("mr"): return "marathi"
        if lang.startswith("hi"): return "hindi"
    except:
        return "english"
    return "english"

# -------- PAGE CONFIG --------
st.set_page_config(page_title="Life Unstuck AI", layout="wide")

# -------- STYLES --------
st.markdown("""
<style>
body { background: linear-gradient(135deg,#e8f0ff,#c7d6ff); font-family:'Segoe UI'; }
.header-box { display:flex; align-items:center; gap:16px; background:#c7d9ff;
              border:1px solid #8fb0ff; padding:16px; border-radius:14px; }
.card { background:#fff; border:1px solid #d8e7ff; padding:18px; border-radius:12px; }
.user-bubble { background:#e5efff; padding:12px; border-radius:12px; border-left:4px solid #2979ff; }
.bot-bubble { background:#f1f7ff; padding:12px; border-radius:12px; border-left:4px solid #0288d1; white-space: pre-wrap; }
footer { position:fixed; bottom:0; width:100%; background:rgba(255,255,255,0.85);
         text-align:center; padding:6px; font-size:13px; }
</style>
""", unsafe_allow_html=True)

# -------- HEADER --------
st.markdown(f"""
<div class="header-box">
    <div>{SVG_LOGO}</div>
    <div>
        <h2 style="margin:0;">✨ Life Unstuck AI</h2>
        <p style="margin:0;color:#333;">Gemini 2.5 Flash + CrewAI</p>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# -------- INPUT CARD --------
st.markdown("<div class='card'>", unsafe_allow_html=True)

user_text = st.text_area("Write your problem:", placeholder="Type here…")
image_file = st.file_uploader("Upload image (optional)", type=["png","jpg","jpeg"])

submitted = st.button("Get Help", use_container_width=True)

st.markdown("</div>", unsafe_allow_html=True)

# -------- PROCESSING --------
if submitted:
    if not user_text.strip() and image_file is None:
        st.warning("Please type something or upload an image.")
    else:
        image_bytes = image_file.read() if image_file else None

        with st.spinner("Thinking…"):
            final_answer = run_multi_agents("general", user_text, image_bytes)

        final_vertical = final_answer.replace("\n", "<br>")

        st.markdown(f"<div class='user-bubble'><b>You:</b><br>{user_text}</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='bot-bubble'><b>Life Unstuck AI:</b><br>{final_vertical}</div>", unsafe_allow_html=True)


# -------------------------------------------------------------------
# FOOTER
st.markdown("""
<footer>
  Life Unstuck AI • Built with ❤️ by RK • Gemini + CrewAI
</footer>
""", unsafe_allow_html=True)
