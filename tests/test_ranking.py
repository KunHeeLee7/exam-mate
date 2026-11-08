import unittest
import pandas as pd
from core.models import Exam
from services.grading import grade
from services.statistics import wrong_answer_ranking
from agent.tools import lookup

class RankingTests(unittest.TestCase):
    def test_second_question_and_ties(self):
        exam=Exam({n:{"answer":1,"points":2} for n in [1,2,3]}, {n:{"number":n,"text":"Test question", "passage":"", "listening":False} for n in [1,2,3]})
        r=grade(exam,pd.DataFrame([[0,0,0],[0,0,1],[1,0,0]],index=["A","B","C"],columns=[1,2,3]))
        ranking=wrong_answer_ranking(r)
        self.assertEqual([x["문항번호"] for x in ranking],[2,1,3])
        self.assertEqual(ranking[1]["동률문항"],[1,3])
        second=lookup(r,"ranked","2")
        self.assertEqual(second["문항"]["number"],1)
        self.assertEqual(second["선택순번"]["오답수"],2)
        self.assertIn("error",lookup(r,"ranked","4"))
