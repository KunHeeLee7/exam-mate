import hashlib
import streamlit as st
from core.session import reset
from core.config import settings
from services.exam_parser import parse_exam
from services.grading import load_responses, grade
from services.statistics import summary, question_stats
from services.excel_export import export_excel
from agent.chatbot import answer

st.markdown("""
<section class="exam-hero compact">
  <div class="exam-eyebrow">EXAM MATE · ANALYSIS</div>
  <h1>시험 분석</h1>
  <p>자료 업로드 → 자동 채점 → 성적 확인과 연습문제 생성</p>
</section>
""", unsafe_allow_html=True)
with st.sidebar:
    st.caption("STEP 01 · 시험 자료 준비")
    st.subheader("시험 자료 업로드")
    st.caption("같은 시험의 파일 3개를 준비해주세요.")
    question=st.file_uploader("문제지 PDF",type=["pdf"],key="questions")
    key=st.file_uploader("정답·배점 PDF",type=["pdf"],key="answers")
    omr=st.file_uploader("학생 OMR 결과 Excel",type=["xlsx"],key="omr")
    payload=[f.getvalue() if f else b"" for f in (question,key,omr)]
    fingerprint=tuple(hashlib.sha256(b).hexdigest() for b in payload)
    if fingerprint!=st.session_state.fingerprint:
        reset()
        st.session_state.fingerprint=fingerprint
    if st.button("분석 시작",type="primary",disabled=not all(payload),use_container_width=True):
        reset()
        try:
            with st.spinner("정답표를 읽고 채점하는 중입니다…"):
                result=grade(parse_exam(payload[0],payload[1]),load_responses(payload[2]))
                excel=export_excel(result)
                st.session_state.result=result
                st.session_state.excel=excel
            st.success("채점이 완료됐습니다.")
        except Exception as exc:
            st.error(str(exc) if isinstance(exc,ValueError) else "파일을 처리하지 못했습니다. 파일이 손상되지 않았는지 확인해주세요.")
    st.caption("분석에는 약 20초까지 소요될 수 있습니다. 파일 크기에 따라 더 걸릴 수 있어요.")
    # 결과 데이터에서 현재 내보내기 코드로 재생성해, 세션에 남은 이전 Excel을 재사용하지 않는다.
    download_data = export_excel(st.session_state.result) if st.session_state.result is not None else b""
    st.download_button("결과 Excel 다운로드",data=download_data,file_name="exam-mate-results.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",disabled=st.session_state.result is None,use_container_width=True)

result=st.session_state.result
if result is None:
    st.info("왼쪽에 파일 3개를 올리고 ‘분석 시작’을 눌러주세요.")
    st.chat_input("채점이 끝나면 질문할 수 있어요",disabled=True)
    st.stop()
s=summary(result)
cols=st.columns(4)
for col,label,value in zip(cols,["학생 수","평균","중앙값","표준편차"],[str(s["학생수"])+"명",f'{s["평균"]:.2f}점',f'{s["중앙값"]:.2f}점',f'{s["표준편차"]:.2f}']):
    col.metric(label,value)
st.caption("표준편차는 업로드된 전체 학생을 모집단으로 계산합니다. 오답 순위 동률은 문항 번호순으로 표시합니다.")
with st.expander("학생별 점수와 문항별 분석 보기"):
    st.dataframe(result.scores.reset_index(),hide_index=True,use_container_width=True)
    st.dataframe(question_stats(result).sort_values(["오답수","문항"],ascending=[False,True]),hide_index=True,use_container_width=True)
st.subheader("시험 결과에 대해 물어보세요")
st.caption("예: 평균과 중앙값은? · 가장 성적이 낮은 학생은? · 가장 많이 틀린 유형의 문제를 만들어줘")
for m in st.session_state.messages:
    with st.chat_message(m["role"]): st.markdown(m["content"])
if prompt:=st.chat_input("성적 분석 또는 연습문제 요청",max_chars=4000):
    st.session_state.messages.append({"role":"user","content":prompt})
    with st.chat_message("user"): st.markdown(prompt)
    with st.chat_message("assistant"):
        try:
            api_key,model=settings()
            with st.spinner("시험 자료를 확인하고 있어요…"):
                response=answer(result,st.session_state.messages,api_key,model)
        except Exception:
            response="답변 요청을 완료하지 못했습니다. API 설정이나 연결 상태를 확인하고 다시 시도해주세요."
        st.markdown(response)
    st.session_state.messages.append({"role":"assistant","content":response})
