import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

api_key = os.environ.get("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

def get_responses(prompt, model="gpt-5-mini"):
    response = client.responses.create(
        model=model,
        tools=[{'type':'web_search_preview'}],  # 웹 검색 도구 활성화
        input=prompt
    )

    return response.output_text

if __name__ == "__main__":
    prompt = """
        https://platform.openai.com/docs/api-reference/responses/create 
        를 읽어서 Responses API에 대해 요약 정리해주세요. 
    """

    output = get_responses(prompt)
    print(output)

