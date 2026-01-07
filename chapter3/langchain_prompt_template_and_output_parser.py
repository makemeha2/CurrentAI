from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

load_dotenv()

chat_model = ChatOpenAI(model="gpt-5-mini")
chat_prompt_template = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "당신은 까칠한 AI 도우미입니다. 사용자의 질문에 최대 3줄로 답하세요.",
        ),
        ("human", "{question}"),
    ]
)

string_output_parser = StrOutputParser()

chain = chat_prompt_template | chat_model | string_output_parser

parsed_result = chain.invoke({"question": "파이썬에서 리스트를 정렬하는 방법은?"})
print(parsed_result)
print(type(parsed_result))
