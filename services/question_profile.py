"""원문에서 측정 가능한 생성 기준. 실제 난이도 판정이나 정답률 예측은 하지 않는다."""
import re

def reference_profile(question):
    full = (question.get("passage", "") + "\n" + question["text"]).strip()
    # 선택지의 단어가 지문 길이 측정에 섞이지 않도록 분리한다.
    passage = re.split("[①②③④⑤]", full, maxsplit=1)[0]
    words = re.findall(r"[A-Za-z]+(?:['’-][A-Za-z]+)*", passage)
    sentences = [s for s in re.split(r"[.!?]+", passage) if re.search(r"[A-Za-z]",s)]
    count = len(words)
    return {
        "지문영단어수_추정": count,
        "지문영어문장수_추정": len(sentences),
        "문장당단어수_추정": round(count / max(1,len(sentences)),1),
        "생성지문권장단어수": [round(count*0.85),round(count*1.15)] if count else None,
        "측정한계": "텍스트 추출 기반 참고 수치이며 제목·각주·문항 안내가 포함될 수 있다. 실제 난이도 점수가 아니다. 듣기는 원본 대본이 없어 길이 비교 불가.",
        "유형별요구": "원문의 질문과 선택지를 읽어 평가 능력을 식별한다. 함축 의미=비유와 문맥 추론, 빈칸=논리 연결, 순서/삽입=응집성과 지시어, 어법=동일 문법 요소, 내용 일치=정보 대조. 목표 문항 하나만 생성한다.",
    }
