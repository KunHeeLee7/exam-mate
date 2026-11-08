import unittest
from agent.chatbot import generation_intent
from services.question_profile import source_contract
from agent.question_generator import validate
class GenerationRoutingTests(unittest.TestCase):
 def test_retry_stays_in_generation(self):
  history=[{"role":"user","content":"33번 문제 만들어줘"},{"role":"assistant","content":"실패"},{"role":"user","content":"다시"}]
  requested,prompt=generation_intent(history)
  self.assertTrue(requested)
  self.assertIn("33번",prompt)
 def test_missing_shared_instruction(self):
  self.assertEqual(source_contract({"number":33,"text":"33. An English passage"})["type"],"Blank inference")
 def test_missing_blank_is_rejected(self):
  ref={"문항":{"number":33,"text":"33. Passage","listening":False},"생성참고기준":{"생성지문권장단어수":None}}
  errors=validate({"type":"Blank inference","passage":"A plain passage.","question":"What is the main idea?","target":"","choices":["A","B","C","D","E"],"answer":1,"explanation":"설명","distractor_explanations":["해설"]*5},ref)
  self.assertTrue(any("real ______ blank" in e for e in errors))

 def test_explicit_number_does_not_depend_on_model_selection(self):
  from unittest.mock import patch
  from agent.chatbot import answer
  with patch('agent.chatbot.OpenAI'), patch('agent.chatbot.lookup',return_value={"문항":{"number":33}}) as lookup_mock, patch('agent.chatbot.generate',return_value="generated") as generator:
   self.assertEqual(answer(object(),[{"role":"user","content":"33번 문제 만들어줘"}],"test-key","test-model"),"generated")
   self.assertEqual(lookup_mock.call_args.args[1:],("question","33"))
   self.assertEqual(generator.call_args.args[2]["문항"]["number"],33)
