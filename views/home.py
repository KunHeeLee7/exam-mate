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
st.markdown("- 수능 영어 **홀수형 문제지 PDF**\n- 같은 시험의 **정답·배점 PDF**\n- **학생명, Q01~Q45** 열로 구성된 학생 응답 Excel")
st.info("현재 텍스트가 포함된 수능 영어 45문항·100점 형식을 지원합니다. 업로드한 자료와 대화는 현재 세션에서만 사용합니다.")
