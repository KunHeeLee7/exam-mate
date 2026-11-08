import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parents[1] / ".env")

def settings():
    import streamlit as st
    def get(name, default=""):
        value = os.getenv(name)
        if value:
            return value
        try:
            return str(st.secrets.get(name, default))
        except (FileNotFoundError, st.errors.StreamlitSecretNotFoundError):
            return default
    return get("OPENAI_API_KEY"), get("OPENAI_MODEL", "gpt-4.1-mini")
