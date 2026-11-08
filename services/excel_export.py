from io import BytesIO
from openpyxl.styles import Font, PatternFill, Alignment
from openpyxl.utils import get_column_letter
import pandas as pd
from services.statistics import summary, question_stats

def export_excel(result):
    output = BytesIO()
    stats = summary(result)
    overview = pd.DataFrame({"항목": list(stats), "값": [", ".join(map(str,v)) if isinstance(v,list) else v for v in stats.values()]})
    details = result.correct.rename(columns=lambda n:f"Q{n:02d}").replace({True:"O",False:"X"})
    details.insert(0, "점수", result.scores)
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        overview.to_excel(writer, sheet_name="전체 성적 통계", index=False, startrow=3)
        first = writer.book["전체 성적 통계"]
        first.merge_cells("A1:F1")
        first["A1"] = "아래 시트 탭에서 학생별 채점 결과 · 문항별 분석 · 학생 응답도 확인하세요!"
        first["A1"].font = Font(bold=True, color="17365D", size=12)
        first["A1"].fill = PatternFill("solid", fgColor="DBEAFE")
        first["A1"].alignment = Alignment(wrap_text=True, vertical="center")
        first.row_dimensions[1].height = 36
        for col, name in zip(["A", "C", "E"], ["학생별 채점 결과", "문항별 분석", "학생 응답"]):
            cell = first[f"{col}2"]
            cell.value = name + " →"
            cell.hyperlink = "#'" + name + "'!A1"
            cell.font = Font(color="2563EB", underline="single")
        details.to_excel(writer, sheet_name="학생별 채점 결과")
        question_stats(result).to_excel(writer, sheet_name="문항별 분석", index=False)
        result.responses.rename(columns=lambda n:f"Q{n:02d}").to_excel(writer, sheet_name="학생 응답")
        for sheet in writer.book:
            sheet.freeze_panes = "B5" if sheet.title == "전체 성적 통계" else "B2"
            sheet.auto_filter.ref = f"A4:B{sheet.max_row}" if sheet.title == "전체 성적 통계" else sheet.dimensions
            for index, col in enumerate(sheet.columns, 1):
                sheet.column_dimensions[get_column_letter(index)].width = min(45,max(12,max(len(str(c.value or "")) for c in col)+3))
                for cell in col:
                    if cell.data_type == "f":
                        cell.data_type = "s"
    return output.getvalue()
