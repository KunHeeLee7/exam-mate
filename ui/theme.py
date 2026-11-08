"""앱 전체의 배경, 카드와 전환 효과."""
import streamlit as st


def apply_theme():
    st.markdown("""
<style>
:root { --exam-ink: #172554; --exam-muted: #526581; --exam-line: #dce5f2; }
html, body, #root,
[data-testid="stApp"], [data-testid="stAppViewContainer"],
[data-testid="stMain"], [data-testid="stHeader"],
[data-testid="stNavigation"], [data-testid="stTopNav"],
[data-testid="stTopNavLinkContainer"], [data-testid="stTopNavSection"],
[data-testid="stToolbar"] {
    background: #edf3fc !important;
    background-image: none !important;
}
[data-testid="stHeader"], [data-testid="stTopNav"], [data-testid="stNavigation"] {
    border-bottom: none !important; box-shadow: none !important;
}
[data-testid="stMainBlockContainer"] { max-width: 1180px; padding-top: 2.5rem; padding-bottom: 4rem; }
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #f6f9ff 0%, #eaf1fc 100%);
    border-right: 1px solid #d5e0ef;
    box-shadow: 8px 0 32px rgba(30,64,175,.045);
}
[data-testid="stSidebar"][aria-expanded="true"] { animation: sidebar-reveal .42s cubic-bezier(.22,1,.36,1) both; }
[data-testid="stSidebarContent"] { animation: content-reveal .45s ease-out both; }
@keyframes sidebar-reveal {
    from { opacity: 0; transform: translateX(-24px); }
    to { opacity: 1; transform: translateX(0); }
}
@keyframes content-reveal {
    from { opacity: 0; } to { opacity: 1; }
}
.exam-hero {
    padding: clamp(24px,4vw,48px); margin: .5rem 0 1.7rem;
    border: 1px solid rgba(255,255,255,.85); border-radius: 4px;
    background: linear-gradient(120deg, #132c5c 0%, #214b92 65%, #3868b5 100%);
    box-shadow: 0 18px 45px rgba(30,58,138,.14); color: white;
    position: relative; overflow: hidden;
}
.exam-hero:after {
    content: ""; position: absolute; width: 280px; height: 280px;
    border: 44px solid rgba(255,255,255,.045); border-radius: 50%;
    right: -70px; top: -120px; pointer-events: none;
}
.exam-eyebrow { font-size: .75rem; letter-spacing: .16em; font-weight: 700; color: #bfdbfe; margin-bottom: 16px; }
.exam-hero h1 { color: white; font-size: clamp(1.9rem,3.5vw,3rem); letter-spacing: -.045em; line-height: 1.25; margin: 0 0 16px; padding: 0; }
.exam-hero p { color: #e0eaff; max-width: 620px; font-size: 1rem; line-height: 1.8; margin: 0; }
.exam-hero.compact { padding: 26px 32px; margin-bottom: 1.4rem; }
.exam-hero.compact h1 { font-size: 2rem; }
.exam-card {
    min-height: 182px; padding: 24px; margin: 12px 0 22px;
    border: 1px solid var(--exam-line); border-radius: 3px;
    box-shadow: 0 4px 14px rgba(30,58,138,.03);
    background-color: #fff;
    background-size: cover;
    background-position: center right;
    background-repeat: no-repeat;
}
.exam-card h3, .exam-card p { position: relative; }
.exam-card .number { color: #2563eb; font-size: .75rem; font-weight: 700; letter-spacing: .1em; }
.exam-card h3 { color: var(--exam-ink); font-size: 1.12rem; margin: 12px 0 10px; padding: 0; }
.exam-card p { color: var(--exam-muted); line-height: 1.7; font-size: .94rem; margin: 0; }
[data-testid="stExpander"], [data-testid="stMetric"] {
    background: rgba(255,255,255,.88); border: 1px solid var(--exam-line); border-radius: 3px;
}
[data-testid="stMetric"] { padding: 16px 20px; }
[data-testid="stFileUploaderDropzone"] { background: rgba(255,255,255,.88); border: 1px dashed #b0c2dd; border-radius: 3px; }
[data-testid="stChatMessage"] { border: 1px solid var(--exam-line); background: rgba(255,255,255,.92); border-radius: 3px; }
[data-testid="stBottomBlockContainer"] { background: transparent; }
.stButton button, .stDownloadButton button { border-radius: 3px; transition: box-shadow .2s ease, background-color .2s ease; }
.stButton button:hover, .stDownloadButton button:hover { box-shadow: 0 4px 14px rgba(37,99,235,.12); }
@media (max-width: 640px) {
    [data-testid="stMainBlockContainer"] { padding-top: 1.5rem; }
    .exam-card { min-height: auto; margin-bottom: 8px; }
    .exam-hero.compact { padding: 24px; }
}
@media (prefers-reduced-motion: reduce) {
    [data-testid="stSidebar"], [data-testid="stSidebarContent"] { animation: none !important; }
    .stButton button, .stDownloadButton button { transition: none; }
}
</style>
""", unsafe_allow_html=True)
