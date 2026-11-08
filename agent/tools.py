import re
from services.statistics import summary, question_stats

TOOLS = [{"type":"function","function":{"name":"lookup_exam","description":"채점 데이터 조회. overview는 전체 통계, student는 특정 학생, question은 문항과 공유 지문, hardest는 최다오답 문항 및 원문을 반환한다.","parameters":{"type":"object","properties":{"kind":{"type":"string","enum":["overview","student","question","hardest"]},"identifier":{"type":"string","description":"학생 식별자 또는 문항 번호. 전체 통계는 빈 문자열."}},"required":["kind","identifier"],"additionalProperties":False},"strict":True}}]

def lookup(result, kind, identifier=""):
    if kind == "overview":
        return summary(result)
    if kind == "student":
        if identifier in result.scores.index:
            ids = [identifier]
        else:
            wanted = re.sub(r"[^0-9]", "", identifier)
            ids = [s for s in result.scores.index if wanted and re.sub(r"[^0-9]", "", s)==wanted]
        if len(ids)!=1:
            return {"error":"학생을 유일하게 찾을 수 없습니다. 정확한 학생 식별자를 확인해주세요."}
        student = ids[0]
        return {"학생":student,"점수":int(result.scores.loc[student]),"오답문항":[int(n) for n in result.correct.columns[~result.correct.loc[student]]]}
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
        return {"문항":result.exam.questions[n],"정답정보":result.exam.answers[n],
                "오답수":int((~result.correct[n]).sum()),"최다오답동률문항":stats["최다오답문항"] if kind=="hardest" else []}
    return {"error":"지원되지 않는 조회입니다."}
