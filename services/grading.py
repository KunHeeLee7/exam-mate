import re
from io import BytesIO
import pandas as pd
from core.models import Result

def load_responses(data):
    df = pd.read_excel(BytesIO(data), dtype=object).dropna(how="all")
    if df.empty:
        raise ValueError("학생 응답이 없습니다.")
    df.columns = [str(c).strip() for c in df.columns]
    names = next((c for c in ["학생명", "학생번호", "이름", "학생 번호"] if c in df), None)
    if names is None:
        raise ValueError("Excel에 학생명 또는 학생번호 열이 필요합니다.")
    ids = df[names].map(lambda x: "" if pd.isna(x) else str(x).strip())
    if ids.eq("").any() or ids.duplicated().any():
        raise ValueError("학생 식별자는 비어 있거나 중복될 수 없습니다.")
    cols = {}
    for col in df.columns:
        m = re.fullmatch(r"(?:Q|q)?0*(\d{1,2})(?:번)?", col)
        if m:
            n = int(m[1])
            if n in cols:
                raise ValueError("문항 열이 중복되었습니다.")
            cols[n] = col
    if set(cols) != set(range(1,46)):
        raise ValueError("Q01~Q45의 45개 응답 열이 필요합니다.")
    answers = df[[cols[n] for n in range(1,46)]].copy()
    answers.columns = range(1,46)
    answers.index = ids
    answers.index.name = "학생명"
    for col in answers:
        raw = answers[col].replace({"①":1,"②":2,"③":3,"④":4,"⑤":5})
        numeric = pd.to_numeric(raw, errors="coerce")
        blank = raw.isna() | raw.astype(str).str.strip().eq("")
        invalid = (~blank) & (~numeric.isin([0,1,2,3,4,5]))
        if invalid.any():
            raise ValueError(f"{col}번 문항에 0~5 이외의 응답이 있습니다. 빈칸·0은 미응답입니다.")
        answers[col] = numeric.fillna(0).astype(int)
    return answers

def grade(exam, responses):
    correct = responses.eq(pd.Series({n:v["answer"] for n,v in exam.answers.items()}), axis="columns")
    scores = correct.mul(pd.Series({n:v["points"] for n,v in exam.answers.items()}), axis="columns").sum(axis=1).astype(int)
    scores.name = "점수"
    return Result(exam, responses, correct, scores)
