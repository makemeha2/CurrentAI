import asyncio
import os

from anthropic import AsyncAnthropic
from dotenv import load_dotenv
from openai import AsyncOpenAI

load_dotenv()

openai_client = AsyncOpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
claude_client = AsyncAnthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

async def call_async_openai(prompt: str, model: str = "gpt-5-mini") -> str :
    response = await openai_client.chat.completions.create(
        model=model,
        messages=[{"role":"user", "content": prompt}]
    )

    return response.choices[0].message.content # type: ignore

async def call_async_claude(prompt: str, model: str = "claude-3-5-haiku-latest") -> str :
    response = await claude_client.messages.create(
        model=model, max_tokens=1000, messages=[{"role": "user", "content": prompt}]
    )

    return response.content[0].text # type: ignore

async def main():
    print("동시에 API 호출하기")
    prompt = "비동기 프로그래밍에 대해 두세 문장으로 설명해주세요."

    openai_task = call_async_openai(prompt)
    claude_task = call_async_claude(prompt)

    openai_response, claude_response = await asyncio.gather(openai_task, claude_task)
    print(f"OpenAI 응답 : {openai_response}")
    print(f"Claude 응답 : {claude_response}")

if __name__ == "__main__":
    asyncio.run(main())