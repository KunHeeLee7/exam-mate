import unittest
import pandas as pd
from core.models import Exam
from services.grading import grade
from agent.tools import lookup

class DataQueryTests(unittest.TestCase):
    def setUp(self):
        self.r=grade(Exam({1:{"answer":1,"points":2},2:{"answer":2,"points":3}},{}),pd.DataFrame([[1,2],[1,2],[1,0]],index=["A","B","C"],columns=[1,2]))
    def test_extremes_include_all_ties(self):
        s=lookup(self.r,"overview")
        self.assertEqual((s["최고점"],s["최고점학생"]),(5,["A","B"]))
        self.assertEqual((s["최저점"],s["최저점학생"]),(2,["C"]))
        self.assertEqual([r["공동순위"] for r in lookup(self.r,"scores")["학생별결과"]],[1,1,3])
    def test_question_distribution_and_student_responses(self):
        q=lookup(self.r,"question_analysis","2")["문항별결과"][0]
        self.assertAlmostEqual(q["오답률"],1/3)
        self.assertEqual(q["응답분포"]["0"],1)
        self.assertEqual(q["오답학생"],["C"])
        a=lookup(self.r,"student_responses","C")["문항별응답"]
        self.assertEqual(a[1]["학생응답"],0)
        self.assertFalse(a[1]["정답여부"])
        self.assertEqual(sum(x["획득점수"] for x in a),2)
