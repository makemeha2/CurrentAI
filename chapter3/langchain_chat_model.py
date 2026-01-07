import random

from dotenv import load_dotenv
from langchain.chat_models import init_chat_model

load_dotenv()

if random.random() < 0.5:
    print("gpt-5-mini selected")
    model = init_chat_model("gpt-5-mini", model_provider="openai")
else:
    print("claude-sonnet-4-20250514 selected")
    model = init_chat_model("claude-sonnet-4-20250514", model_provider="anthropic")

result = model.invoke("한국의 왕 세종대왕의 업적 3가지를 각각 한줄로 설명하시오.")
print(result.content)