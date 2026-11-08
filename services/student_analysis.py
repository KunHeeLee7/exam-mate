"""채점과 문항 내용을 근거로 한 학습 분석 자료. 개인적 원인은 판단하지 않는다."""
from collections import defaultdict
import re

def question_type(q):
    if q.get("listening"):
        return "듣기"
    stem=q.get("text","")[:200]
    for pattern,label in [("빈칸","빈칸 추론"),("순서|배열","글의 순서"),("들어가기에|넣기에","문장 삽입"),("어법","어법"),("낱말|어휘","문맥상 어휘"),("밑줄|의미하는","표현·함축 의미"),("일치|내용으로","내용 이해"),("요약","요약"),("제목|주제|요지|주장|목적","중심 내용 파악")]:
        if re.search(pattern,stem):return label
    return "기타 독해"

def analyze_student(result, student):
    buckets=defaultdict(lambda:{"전체문항수":0,"오답수":0,"미응답수":0,"감점":0,"오답문항":[]})
    wrong=[]
    for n in result.correct.columns:
        n=int(n);q=result.exam.questions.get(n,{"number":n,"text":""})
        b=buckets[question_type(q)];b["전체문항수"]+=1
        if not bool(result.correct.loc[student,n]):
            b["오답수"]+=1;b["오답문항"].append(n)
            b["감점"]+=result.exam.answers[n]["points"]
            b["미응답수"]+=int(result.responses.loc[student,n]==0)
            wrong.append(n)
    total=sum(v["points"] for v in result.exam.answers.values())
    categories=[]
    for label,b in buckets.items():
        categories.append({"유형":label,**b,"오답률":round(b["오답수"]/b["전체문항수"],3)})
    categories.sort(key=lambda x:(-x["감점"],-x["오답률"]))
    examples=[]
    for b in categories:
        for n in b["오답문항"][:1]:
            q=result.exam.questions.get(n,{})
            examples.append({"문항번호":n,"유형":b["유형"],"학생응답":int(result.responses.loc[student,n]),"정답정보":result.exam.answers[n],"문항텍스트":q.get("text",""),"공유지문":q.get("passage","")})
        if len(examples)>=3:break
    return {"학생":student,"점수":int(result.scores.loc[student]),"총점":total,
            "평균":float(result.scores.mean()),"오답문항":wrong,
            "미응답문항":[n for n in wrong if result.responses.loc[student,n]==0],
            "유형별분석":categories,"대표오답":examples,
            "분석한계":"유형은 문항 안내문에서 자동 분류한 참고값. 출석·공부량·심리 상태·시험 준비 상황은 알 수 없음. 오답만으로 실제 원인을 확정할 수 없음."}
