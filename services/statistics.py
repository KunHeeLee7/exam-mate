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
