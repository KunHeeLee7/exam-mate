import re
from io import BytesIO
from pypdf import PdfReader
from core.models import Exam

CIRCLED = dict(zip("①②③④⑤", range(1, 6)))

def pdf_text(data):
    reader = PdfReader(BytesIO(data))
    if len(reader.pages) > 50:
        raise ValueError("50페이지 이하의 수능 영어 PDF를 사용해주세요.")
    text = "\n".join(page.extract_text() or "" for page in reader.pages)
    if not text.strip():
        raise ValueError("텍스트를 추출할 수 없습니다. 스캔본 대신 텍스트 PDF를 사용해주세요.")
    return text

def parse_answers(data):
    text = pdf_text(data)
    answers = {}
    for m in re.finditer(r"(\d(?:\s*\d)?)\s*([①②③④⑤])\s*([23])", text):
        number = int(re.sub(r"\s", "", m[1]))
        if number in answers:
            raise ValueError("정답표에 중복 문항이 있습니다. 한 가지 유형의 정답표 하나를 업로드해주세요.")
        answers[number] = {"answer": CIRCLED[m[2]], "points": int(m[3])}
    if set(answers) != set(range(1, 46)) or sum(x["points"] for x in answers.values()) != 100:
        raise ValueError("정답표에서 45문항·총 100점을 확인하지 못했습니다. 정답 PDF 형식을 확인해주세요.")
    return dict(sorted(answers.items()))

def parse_questions(data):
    text = pdf_text(data)
    marks = list(re.finditer(r"(?m)^\s*(\d{1,2})\.\s+", text))
    groups = list(re.finditer(r"\[(\d{1,2})\s*[～~–-]\s*(\d{1,2})\]", text))
    shared = {}
    for g in groups:
        following = next((m for m in marks if m.start() > g.end()), None)
        if following:
            for n in range(int(g[1]), int(g[2]) + 1):
                shared[n] = text[g.start():following.start()].strip()
    questions = {}
    for i, m in enumerate(marks):
        n = int(m[1])
        if not 1 <= n <= 45:
            continue
        end = marks[i+1].start() if i+1 < len(marks) else len(text)
        between = [g.start() for g in groups if m.end() < g.start() < end]
        if between:
            end = min(between)
        questions[n] = {"number": n, "text": text[m.start():end].strip(),
                        "passage": shared.get(n, ""), "listening": n <= 17}
    if set(questions) != set(range(1, 46)):
        raise ValueError("문제지에서 1~45번을 모두 구분하지 못했습니다. 수능 영어 문제지인지 확인해주세요.")
    return questions

def parse_exam(question_pdf, answer_pdf):
    return Exam(parse_answers(answer_pdf), parse_questions(question_pdf))
