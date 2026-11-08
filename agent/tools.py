import re
from services.student_analysis import analyze_student
from services.question_profile import reference_profile
from services.statistics import summary, question_stats, wrong_answer_ranking

TOOLS = [{"type":"function","function":{"name":"lookup_exam","description":"채점 데이터 조회. overview는 전체 통계, student는 특정 학생 점수, student_analysis는 성적이 저조한 이유·약점·학습 조언을 위한 유형별 오답 분석, question은 문항과 공유 지문, hardest는 1번째 최다오답 문항만 반환한다. 두 번째, 세 번째, N번째, 상위 목록 등 오답 순위 질문에는 반드시 ranked를 사용한다. ranked는 전체 순위와 identifier에 지정한 순번의 문항 원문을 반환한다.","parameters":{"type":"object","properties":{"kind":{"type":"string","enum":["overview","student","student_analysis","question","hardest","ranked"]},"identifier":{"type":"string","description":"학생 식별자 또는 문항 번호. ranked일 때는 요청 순번을 숫자 문자열로 전달(예: 두 번째는 2). 전체 순위 목록은 빈 문자열. 전체 통계는 빈 문자열."}},"required":["kind","identifier"],"additionalProperties":False},"strict":True}}]

def lookup(result, kind, identifier=""):
    if kind == "overview":
        return summary(result)
    if kind in ("student", "student_analysis"):
        if identifier in result.scores.index:
            ids = [identifier]
        else:
            wanted = re.sub(r"[^0-9]", "", identifier)
            ids = [s for s in result.scores.index if wanted and re.sub(r"[^0-9]", "", s)==wanted]
        if len(ids)!=1:
            return {"error":"학생을 유일하게 찾을 수 없습니다. 정확한 학생 식별자를 확인해주세요."}
        student = ids[0]
        if kind == "student_analysis":
            return analyze_student(result, student)
        return {"학생":student,"점수":int(result.scores.loc[student]),"오답문항":[int(n) for n in result.correct.columns[~result.correct.loc[student]]]}
    if kind == "ranked":
        ranking = wrong_answer_ranking(result)
        metadata = {"정렬기준":"오답 수 내림차순, 동률이면 문항 번호 오름차순. 정렬순번이며 동률 공동순위와 다름.", "전체오답순위":ranking}
        if not identifier:
            return metadata
        try:
            position=int(identifier)
        except ValueError:
            return {"error":"정렬순번을 1 이상의 정수로 입력해주세요."}
        if not 1<=position<=len(ranking):
            return {"error":"요청 순번의 문항이 없습니다."}
        selected=ranking[position-1]
        if selected["오답수"] == 0:
            return {**metadata,"선택순번":selected,"안내":"이 순번의 문항은 모든 학생이 맞혔습니다."}
        detail=lookup(result,"question",str(selected["문항번호"]))
        return {**metadata,**detail,"선택순번":selected}
    if kind in ("question", "hardest"):
        stats=summary(result)
        if kind == "hardest":
            n=min(stats["최다오답문항"])
            if stats["최다오답수"]==0:
                return {"error":"모든 학생이 만점을 받아 오답 문항이 없습니다."}
        else:
            try: n=int(identifier)
            except ValueError: return {"error":"문항 번호는 정수여야 합니다."}
        if n not in result.exam.questions:
            return {"error":"문항이 없습니다."}
        return {"문항":result.exam.questions[n],"정답정보":result.exam.answers[n],"생성참고기준":reference_profile(result.exam.questions[n]),
                "오답수":int((~result.correct[n]).sum()),"최다오답동률문항":stats["최다오답문항"] if kind=="hardest" else []}
    return {"error":"지원되지 않는 조회입니다."}
