import copy
import unittest
from agent.question_generator import validate, render

class QuestionLanguageTests(unittest.TestCase):
    def setUp(self):
        self.ref={"문항":{"number":21,"listening":False},"생성참고기준":{"생성지문권장단어수":None}}
        self.data={"type":"Implied meaning", "passage":"Ideas can cross invisible bridges between people.","question":"What does the expression in bold mean?", "target":"invisible bridges", "choices":["Shared understanding","Physical construction","A permanent boundary","An empty road","A private island"],"answer":1,"explanation":"의미를 공유하는 상황입니다.","distractor_explanations":["정답","오답","오답","오답","오답"]}
    def test_english_question_with_korean_explanations_is_valid(self):
        self.assertEqual(validate(self.data,self.ref),[])
        before_explanation=render(self.data,self.ref).split("**정답:")[0]
        self.assertNotRegex(before_explanation,r"[가-힣]")
    def test_mixed_language_is_rejected(self):
        for field in ["type","passage","question","target"]:
            with self.subTest(field=field):
                data=copy.deepcopy(self.data);data[field]+=" 강하게 밀려오는 거대한 파도처럼"
                self.assertTrue(any("English only" in e for e in validate(data,self.ref)))
        data=copy.deepcopy(self.data);data["choices"][0]="Shared 이해"
        self.assertTrue(validate(data,self.ref))
    def test_hangul_jamo_is_rejected(self):
        data=copy.deepcopy(self.data);data["question"]+=" ㄱ"
        self.assertTrue(validate(data,self.ref))
