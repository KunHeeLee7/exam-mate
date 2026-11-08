import streamlit as st
from pathlib import Path
import base64

@st.cache_data
def card_image(name):
    data = (Path(__file__).resolve().parents[1] / "assets" / (name + ".png")).read_bytes()
    return "data:image/png;base64," + base64.b64encode(data).decode("ascii")

st.markdown("""
<section class="exam-hero">
  <div class="exam-eyebrow">EXAM MATE · ENGLISH ASSESSMENT</div>
  <h1>채점부터 다음 수업 준비까지</h1>
  <p>흩어진 시험 결과를 한눈에.<br>학생의 성적을 살펴보고, 다음 학습에 필요한 문제를 준비하세요.</p>
</section>
""", unsafe_allow_html=True)
st.page_link("views/analysis.py",label="시험 분석 시작하기 →",icon="📊")
features = [
    ("01 · UPLOAD", "시험 자료를 올리세요", "문제지, 정답표, 학생 응답 파일을 업로드하면 배점에 맞춰 자동으로 채점합니다."),
    ("02 · ANALYZE", "성적을 한눈에 확인하세요", "학생별 점수와 자주 틀린 문항을 살펴보고, 분석 결과를 Excel로 내려받으세요."),
    ("03 · PRACTICE", "다음 학습을 준비하세요", "성적을 대화로 물어보고, 많이 틀린 유형을 바탕으로 새로운 연습문제를 만드세요."),
]
for col, (number, title, description), image_name in zip(st.columns(3), features, ["upload", "report", "learning"]):
    with col:
        background = f"linear-gradient(90deg, rgba(255,255,255,.97) 0%, rgba(255,255,255,.88) 48%, rgba(255,255,255,.42) 100%), url({card_image(image_name)})"
        st.markdown(f'<article class="exam-card" style="background-image: {background};"><div class="number">{number}</div><h3>{title}</h3><p>{description}</p></article>',unsafe_allow_html=True)
st.divider()
st.subheader("준비할 파일")
st.markdown("- **수능 영어 문제지 PDF**\n- 문제지와 동일한 시험·유형의 **정답·배점 PDF**\n- 아래 열 구성을 갖춘 **학생 응답 Excel(.xlsx)**")
with st.expander("학생 응답 Excel 형식 확인", expanded=True):
    st.markdown("- **첫 번째 시트**를 읽습니다. 학생 한 명을 한 행에 입력해주세요.\n- 학생 식별자 열: `학생명`, `학생번호`, `이름`, `학생 번호` 중 하나\n- 문항 열: **1~45번 전체**가 필요합니다. `Q01`, `Q1`, `q1`, `1`, `1번` 형식을 지원합니다.\n- 응답: **1~5** 또는 **①~⑤**. 빈칸과 0은 미응답으로 채점합니다.\n- 학생 식별자는 비어 있거나 중복되면 안 됩니다.")
    st.dataframe({"학생명":["1학생","2학생"],"Q01":[3,2],"Q02":[2,2],"…":["…","…"],"Q45":[5,4]},hide_index=True)
    st.caption("위 표는 열 구성 예시입니다. 실제 파일에는 45개 문항 열을 모두 넣어주세요.")

st.info("현재 텍스트가 포함된 수능 영어 45문항·100점 형식을 지원합니다. 업로드한 자료와 대화는 현재 세션에서만 사용합니다.")
