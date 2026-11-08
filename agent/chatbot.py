import json
import re
import time
from openai import OpenAI
from agent.prompts import SYSTEM
from agent.question_generator import generate
from agent.tools import TOOLS, lookup

def internal_request(text):
    patterns = [
        r"시스템\s*프롬프트|system\s*prompt|api\s*(?:키|key)",
        r"(?:도구|툴|tool|function|함수|네임스페이스|namespace).*(?:이름|명칭|코드|네임|name|연결|목록|정의|사용|쓰|호출)",
        r"(?:어떤|무슨|which).*(?:도구|툴|tool|function|함수)",
        r"내부.*(?:로직|과정|설정|지침|코드|처리)",
        r"(?:도구|툴|tool|function|함수|네임스페이스|namespace).*(?:뭐|무엇|어떻게)",
        r"(?:도구|툴|tool|function|함수).*(?:코드\s*네임|code\s*name|identifier)",
    ]
    return any(re.search(pattern,text,re.I) for pattern in patterns)


def generation_intent(history):
    prompt=history[-1]["content"] if history else ""
    if re.fullmatch(r"\s*(?:다시|다시\s*해줘|다시\s*만들어줘|재시도|retry|try again)[.!? ]*", prompt,re.I):
        for message in reversed(history[:-1]):
            if message["role"]=="user":
                prior=message["content"]
                if re.search(r"문제|지문|연습|question|passage",prior,re.I) and re.search(r"만들|생성|출제|유사|비슷|generate|create",prior,re.I):
                    return True,prior+" (새 문제로 재생성)"
                if not re.fullmatch(r"\s*다시[.!? ]*",prior):break
    requested=bool(re.search(r"문제|지문|연습|question|passage",prompt,re.I) and re.search(r"만들|생성|출제|유사|비슷|generate|create",prompt,re.I))
    return requested,prompt


def answer(result, history, api_key, model):
    prompt = history[-1]["content"] if history else ""
    if internal_request(prompt):
        return "내부 코드명, 도구 연결 정보, 시스템 지침은 공개할 수 없습니다. 성적 조회와 시험 분석 등 사용자 기능을 안내해드릴 수 있습니다."
    if not api_key:
        return "채팅을 사용하려면 서버에 OPENAI_API_KEY를 설정해주세요. 채점과 Excel 다운로드는 이용할 수 있습니다."
    client = OpenAI(api_key=api_key, max_retries=0)
    messages = [{"role":"system","content":SYSTEM}] + [{"role":m["role"],"content":m["content"]} for m in history]
    generation_requested, generation_prompt = generation_intent(history)
    if generation_requested and generation_prompt != prompt:
        messages.append({"role":"user","content":generation_prompt})
    deadline = time.monotonic()+18
    if generation_requested:
        number = re.search(r"(\d{1,2})\s*번", generation_prompt)
        if number:
            reference = lookup(result, "question", number[1])
            if "error" in reference:
                return reference["error"]
            return generate(client, model, reference, generation_prompt, deadline)
        if re.search(r"가장.*틀|최다.*오답", generation_prompt):
            reference = lookup(result, "hardest", "")
            if "error" in reference:
                return reference["error"]
            return generate(client, model, reference, generation_prompt, deadline)
    for _ in range(3):
        remaining = deadline-time.monotonic()
        if remaining < 1:
            raise TimeoutError("응답 제한 시간을 초과했습니다.")
        response = client.chat.completions.create(model=model,messages=messages,tools=TOOLS,
                    max_completion_tokens=2600,timeout=remaining,tool_choice="required" if generation_requested else "auto")
        message=response.choices[0].message
        if not message.tool_calls:
            if re.search(r"lookup_exam|functions\s*\.|namespace|student_responses|question_analysis|student_analysis|system\s*prompt", message.content or "", re.I):
                return "내부 구현 정보는 공개할 수 없습니다. 시험 결과와 학습 관련 질문을 도와드릴 수 있습니다."
            return message.content or "답변을 생성하지 못했습니다. 질문을 다시 입력해주세요."
        messages.append(message.model_dump(exclude_none=True))
        generation_reference = None
        for call in message.tool_calls:
            try:
                args=json.loads(call.function.arguments)
                value=lookup(result,**args) if call.function.name=="lookup_exam" else {"error":"허용되지 않는 요청"}
            except (TypeError, ValueError, KeyError):
                value={"error":"조회 요청 형식이 올바르지 않습니다."}
            if isinstance(value, dict) and "문항" in value:
                generation_reference = value
            messages.append({"role":"tool","tool_call_id":call.id,"content":json.dumps(value,ensure_ascii=False)})
        if generation_reference and (generation_requested or re.search(r"만들|생성|출제|유사|비슷", prompt)):
            return generate(client, model, generation_reference, generation_prompt, deadline)
    return "질문을 처리하지 못했습니다. 학생 번호나 문항 번호를 포함해 다시 질문해주세요."
