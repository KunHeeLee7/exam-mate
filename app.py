import streamlit as st
from core.session import initialize
from ui.theme import apply_theme

st.set_page_config(page_title="Exam Mate | 우리학원 시험 도우미", page_icon="📘", layout="wide")
apply_theme()
initialize()
st.navigation([st.Page("views/home.py",title="서비스 소개",icon="🏠"),
               st.Page("views/analysis.py",title="시험 분석",icon="📊")],position="top").run()
