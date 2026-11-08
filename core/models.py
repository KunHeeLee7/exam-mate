from dataclasses import dataclass
import pandas as pd

@dataclass
class Exam:
    answers: dict
    questions: dict

@dataclass
class Result:
    exam: Exam
    responses: pd.DataFrame
    correct: pd.DataFrame
    scores: pd.Series
