import os

from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_core.prompts import load_prompt

load_dotenv()

current_dir_path = os.path.dirname(os.path.abspath(__file__))

file_prompt = load_prompt(f"{current_dir_path}/template_example.yaml", encoding="utf-8")
print(file_prompt.format(context="서울은 한국 수도이다", question="수도는?"))

model = init_chat_model("gpt-5-mini", model_provider="openai")
result = model.invoke(
    file_prompt.format(context="서울은 한국 수도이다", question="수도는?")
)

print(result.content)
