import os
from google.api_core.client_options import ClientOptions
from google.ai.generativelanguage import GenerativeServiceClient
from google.ai.generativelanguage_v1beta.types import Part, Content

API_KEY = "AIzaSyBEkn15mooTKbRDtCP5Nc95wP7rugbnorQ"


try:
    client = GenerativeServiceClient(client_options=ClientOptions(api_key=API_KEY))

    resp = client.generate_content(
        model="models/gemini-2.5-flash",
        contents=[Content(parts=[Part(text="Test")])]
    )

    print("KEY IS VALID & SUPPORTS: gemini-2.5-flash")
except Exception as e:
    print("Error:", e)
