import streamlit as st
st.caption("EXAM MATE · 수능 영어 평가 도우미")
st.title("채점부터 다음 수업 준비까지")
st.markdown("수능 영어 시험 결과를 한눈에 살펴보고, 학생들에게 필요한 다음 문제를 준비하세요.")
st.page_link("views/analysis.py",label="시험 분석 시작하기 →",icon="📊")
a,b,c=st.columns(3)
with a:
    st.subheader("01 · 자동 채점")
    st.write("문제지, 정답표, 학생 응답을 올리면 배점에 맞춰 채점합니다.")
with b:
    st.subheader("02 · 성적 한눈에")
    st.write("학생별 점수와 자주 틀린 문항을 살펴보고 Excel로 내려받으세요.")
with c:
    st.subheader("03 · 다음 학습 준비")
    st.write("성적을 질문하고, 가장 많이 틀린 유형의 새로운 연습문제를 만들어보세요.")
st.divider()
st.subheader("준비할 파일")
st.markdown("- **수능 영어 문제지 PDF**\n- 문제지와 동일한 시험·유형의 **정답·배점 PDF**\n- 아래 열 구성을 갖춘 **학생 응답 Excel(.xlsx)**")
with st.expander("학생 응답 Excel 형식 확인", expanded=True):
    st.markdown("- **첫 번째 시트**를 읽습니다. 학생 한 명을 한 행에 입력해주세요.\n- 학생 식별자 열: `학생명`, `학생번호`, `이름`, `학생 번호` 중 하나\n- 문항 열: **1~45번 전체**가 필요합니다. `Q01`, `Q1`, `q1`, `1`, `1번` 형식을 지원합니다.\n- 응답: **1~5** 또는 **①~⑤**. 빈칸과 0은 미응답으로 채점합니다.\n- 학생 식별자는 비어 있거나 중복되면 안 됩니다.")
    st.dataframe({"학생명":["1학생","2학생"],"Q01":[3,2],"Q02":[2,2],"…":["…","…"],"Q45":[5,4]},hide_index=True)
    st.caption("위 표는 열 구성 예시입니다. 실제 파일에는 45개 문항 열을 모두 넣어주세요.")

st.info("현재 텍스트가 포함된 수능 영어 45문항·100점 형식을 지원합니다. 업로드한 자료와 대화는 현재 세션에서만 사용합니다.")
