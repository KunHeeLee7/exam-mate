import unittest
import pandas as pd
from core.models import Exam
from services.grading import grade
from services.statistics import summary
from agent.tools import lookup

class GradingTests(unittest.TestCase):
    def setUp(self):
        self.exam=Exam({1:{"answer":1,"points":2},2:{"answer":2,"points":3}}, {})
    def test_weighted_grading_and_missing(self):
        r=grade(self.exam,pd.DataFrame([[1,2],[1,0],[0,0]],index=["1학생","2학생","3학생"],columns=[1,2]))
        self.assertEqual(r.scores.tolist(),[5,2,0])
        self.assertEqual(summary(r)["중앙값"],2)
        self.assertEqual(lookup(r,"student","2번 학생")["점수"],2)
        self.assertIn("error",lookup(r,"student","87번"))
    def test_ties_and_population_std(self):
        r=grade(self.exam,pd.DataFrame([[0,0],[0,0]],index=["A","B"],columns=[1,2]))
        s=summary(r)
        self.assertEqual(s["최저점학생"],["A","B"])
        self.assertEqual(s["최다오답문항"],[1,2])
        self.assertEqual(s["표준편차"],0)

if __name__=="__main__": unittest.main()
