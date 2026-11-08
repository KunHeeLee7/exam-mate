def summary(result):
    s = result.scores
    wrong = (~result.correct).sum().sort_values(ascending=False, kind="stable")
    highest = int(wrong.max())
    return {"학생수": len(s), "평균": float(s.mean()), "중앙값": float(s.median()),
            "표준편차": float(s.std(ddof=0)), "최저점": int(s.min()),
            "최저점학생": s[s.eq(s.min())].index.tolist(),
            "오답상위3문항": [int(n) for n in wrong.index[:3]],
            "최다오답문항": [int(n) for n in wrong[wrong.eq(highest)].index],
            "최다오답수": highest}

def question_stats(result):
    import pandas as pd
    wrong = (~result.correct).sum()
    return pd.DataFrame({"문항": wrong.index, "정답": [v["answer"] for v in result.exam.answers.values()],
                         "배점": [v["points"] for v in result.exam.answers.values()],
                         "오답수": wrong.values, "오답률": wrong.values / len(result.scores)})


def wrong_answer_ranking(result):
    """오답 수 내림차순, 동률이면 문항 번호 오름차순으로 나열한다."""
    rows = question_stats(result).sort_values(["오답수", "문항"], ascending=[False, True])
    output=[]
    for position, (_, row) in enumerate(rows.iterrows(),1):
        count=int(row["오답수"])
        ties=rows.loc[rows["오답수"].eq(count), "문항"].astype(int).tolist()
        output.append({"정렬순번":position,"문항번호":int(row["문항"]),"오답수":count,
                       "오답률":float(row["오답률"]),"동률문항":ties})
    return output
