import os
from urllib import response

from dotenv import load_dotenv
from openai import OpenAI

# .env 파일에서 환경 변수 로드
load_dotenv()

# 오픈 AI API 키 가져오기
api_key = os.environ.get("OPENAI_API_KEY") 

client = OpenAI(api_key=api_key)

def get_chat_comletion(prompt, model="gpt-5-mini"):
    response = client.chat.completions.create(model=model, messages=[
        {"role": "system", "content": "당신은 친절하고 도움이 되는 AI 비서입니다"},
        {"role": "user", "content": prompt}
    ])

    return response.choices[0].message.content

if __name__ == "__main__" :
    user_prompt = input("AI에게 물어볼 질문을 입력하세요. : ")
    response = get_chat_comletion(user_prompt)
    print("\nAI 응답: ")
    print(response)