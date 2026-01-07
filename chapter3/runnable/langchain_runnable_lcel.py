from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

load_dotenv()

prompt = ChatPromptTemplate.from_template(
    "주어지는 문구에 대하여 100자 이내의 짧은 시를 작성해주세요 : {word}"
)
model = ChatOpenAI(model="gpt-5-mini")
parser = StrOutputParser()

chain = prompt | model | parser

result = chain.invoke({"word": "쇼호스트"})
print(result)