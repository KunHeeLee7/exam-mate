import json
import re
import time
from openai import OpenAI
from agent.prompts import SYSTEM
from agent.question_generator import generate
from agent.tools import TOOLS, lookup

def answer(result, history, api_key, model):
    prompt = history[-1]["content"] if history else ""
    if re.search(r"(?i)(시스템\s*프롬프트|system\s*prompt|api\s*키|api\s*key|어떤\s*(?:tool|도구)|(?:tool|도구).*(?:연결|목록|정의|이름)|내부\s*(?:설정|지침))", prompt):
        return "내부 설정이나 도구 연결 정보는 공개할 수 없습니다. 시험 성적 조회, 오답 분석, 유사 문제 생성을 도와드릴 수 있습니다."
    if not api_key:
        return "채팅을 사용하려면 서버에 OPENAI_API_KEY를 설정해주세요. 채점과 Excel 다운로드는 이용할 수 있습니다."
    client = OpenAI(api_key=api_key, max_retries=0)
    messages = [{"role":"system","content":SYSTEM}] + [{"role":m["role"],"content":m["content"]} for m in history]
    generation_requested = bool(re.search(r"문제|지문|연습|question|passage", prompt, re.I) and re.search(r"만들|생성|출제|유사|비슷|generate|create", prompt, re.I))
    deadline = time.monotonic()+18
    for _ in range(3):
        remaining = deadline-time.monotonic()
        if remaining < 1:
            raise TimeoutError("응답 제한 시간을 초과했습니다.")
        response = client.chat.completions.create(model=model,messages=messages,tools=TOOLS,
                    max_completion_tokens=2600,timeout=remaining,tool_choice="required" if generation_requested else "auto")
        message=response.choices[0].message
        if not message.tool_calls:
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
            return generate(client, model, generation_reference, prompt, deadline)
    return "질문을 처리하지 못했습니다. 학생 번호나 문항 번호를 포함해 다시 질문해주세요."
