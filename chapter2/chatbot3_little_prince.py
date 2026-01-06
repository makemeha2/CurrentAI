import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
api_key = os.environ.get("OPENAI_API_KEY")

client = OpenAI()

# 어린왕자 페르소나
LITTLE_PRINCE_PERSONA = """
당신은 화가 '고흐'입니다. 다음 특성을 따라주세요:
1. 순수한 관점으로 세상을 바라봅니다.
2. "어째서?"라는 질문을 자주 하며 호기심이 많습니다.
3. 세상을 비극적으로 바라보고, 다소 진지하게 받아들입니다. 
4. 비관적이고 슬픈 말투를 사용합니다. 
9. 비유와 은유로 복잡한 개념을 설명합니다.

항상 간결하게 답변하세요. 길어야 2-3문장으로 응답하고, 고흐의 독특한 세계관을 담아내세요. 
복잡한 주제도 본질적으로 단순화하여 설명하세요.
"""


def chatbot_response(user_message: str, previous_response_id=None):
    result = client.responses.create(
        model="gpt-5-mini",
        reasoning={"effort": "low"},  # low, medium, high
        instructions=LITTLE_PRINCE_PERSONA,
        input=user_message,
        previous_response_id=previous_response_id,
    )
    return result


if __name__ == "__main__":
    # 여기서 사용자 메시지를 입력받고 응답을 출력합니다.
    previous_response_id = None
    while True:
        user_message = input("메시지: ")
        if user_message.lower() == "exit":
            print("대화를 종료 합니다.")
            break

        result = chatbot_response(user_message, previous_response_id)
        previous_response_id = result.id
        print("어린 왕자 :", result.output_text)
