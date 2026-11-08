import streamlit as st

def initialize():
    for key, value in {"result": None, "messages": [], "fingerprint": None, "excel": None}.items():
        if key not in st.session_state:
            st.session_state[key] = value

def reset():
    st.session_state.result = None
    st.session_state.messages = []
    st.session_state.excel = None
