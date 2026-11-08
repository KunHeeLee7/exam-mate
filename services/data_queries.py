"""Excel의 각 시트와 동일한 채점 데이터에 대한 조회."""
from services.statistics import question_stats

def score_records(result):
    records=[]
    for student,score in result.scores.items():
        records.append({"학생":str(student),"점수":int(score),
                        "정답수":int(result.correct.loc[student].sum()),
                        "오답수":int((~result.correct.loc[student]).sum()),
                        "공동순위":int(result.scores.rank(method="min",ascending=False).loc[student])})
    return sorted(records,key=lambda x:(-x["점수"],x["학생"]))

def student_response_records(result,student):
    return [{"문항번호":int(n),"학생응답":int(result.responses.loc[student,n]),
             "정답":int(result.exam.answers[n]["answer"]),"배점":int(result.exam.answers[n]["points"]),
             "정답여부":bool(result.correct.loc[student,n]),
             "획득점수":int(result.exam.answers[n]["points"]) if result.correct.loc[student,n] else 0}
            for n in result.responses.columns]

def question_analysis(result,number=None):
    stats=question_stats(result)
    records=[]
    for row in stats.to_dict("records"):
        n=int(row["문항"])
        if number is not None and n!=number:continue
        row={k:(int(v) if k!="오답률" else float(v)) for k,v in row.items()}
        row.update({"학생수":len(result.scores),"정답수":int(result.correct[n].sum()),
                    "정답률":float(result.correct[n].mean()),
                    "응답분포":{str(a):int(result.responses[n].eq(a).sum()) for a in range(6)},
                    "오답학생":result.correct.index[~result.correct[n]].tolist()})
        records.append(row)
    return records
