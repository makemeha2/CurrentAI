# 대화내용을 기억하는 chatbot 만들기

import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

# 오픈 AI API 키 가져오기
api_key = os.environ.get("OPENAI_API_KEY")

client = OpenAI(api_key=api_key)


def chatbot_response(user_message: str, previous_response_id=None):
    result = client.responses.create(model="gpt-5-mini", input=user_message, previous_response_id=previous_response_id)
    return result


if __name__ == "__main__":
    previous_response_id = None

    while True:
        user_message = input("메세지: ")
        if user_message.lower() == "exit":
            print("대화를 종료합니다")
            break

        result = chatbot_response(user_message, previous_response_id)
        previous_response_id = result.id
        print(f"챗봇 : {result.output_text}")  # type: ignore
