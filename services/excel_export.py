from io import BytesIO
import pandas as pd
from services.statistics import summary, question_stats

def export_excel(result):
    output = BytesIO()
    stats = summary(result)
    overview = pd.DataFrame({"항목": list(stats), "값": [", ".join(map(str,v)) if isinstance(v,list) else v for v in stats.values()]})
    details = result.correct.rename(columns=lambda n:f"Q{n:02d}").replace({True:"O",False:"X"})
    details.insert(0, "점수", result.scores)
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        overview.to_excel(writer, sheet_name="전체 성적 통계", index=False)
        details.to_excel(writer, sheet_name="학생별 채점 결과")
        question_stats(result).to_excel(writer, sheet_name="문항별 분석", index=False)
        result.responses.rename(columns=lambda n:f"Q{n:02d}").to_excel(writer, sheet_name="학생 응답")
        for sheet in writer.book:
            sheet.freeze_panes = "B2"
            sheet.auto_filter.ref = sheet.dimensions
            for col in sheet.columns:
                sheet.column_dimensions[col[0].column_letter].width = min(45,max(12,max(len(str(c.value or "")) for c in col)+3))
                for cell in col:
                    if cell.data_type == "f":
                        cell.data_type = "s"
    return output.getvalue()
