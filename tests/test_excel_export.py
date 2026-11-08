import unittest
from io import BytesIO
import pandas as pd
from openpyxl import load_workbook
from core.models import Exam
from services.grading import grade
from services.excel_export import export_excel

class ExcelGuideTests(unittest.TestCase):
    def test_guide_links_and_grading_sheets(self):
        exam=Exam({1:{"answer":1,"points":2},2:{"answer":2,"points":3}}, {})
        result=grade(exam,pd.DataFrame([[1,0]],index=["1학생"],columns=[1,2]))
        book=load_workbook(BytesIO(export_excel(result)))
        self.assertEqual(book.sheetnames,["전체 성적 통계","학생별 채점 결과","문항별 분석","학생 응답"])
        first=book.worksheets[0]
        self.assertIn("아래 시트 탭",first["A1"].value)
        self.assertEqual(first["A4"].value,"항목")
        for row,name in zip([2,4,6],book.sheetnames[1:]):
            self.assertEqual(first[f"E{row}"].hyperlink.target,f"#'{name}'!A1")
        self.assertEqual(book["학생별 채점 결과"]["B2"].value,2)
