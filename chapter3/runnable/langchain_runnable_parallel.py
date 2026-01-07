from dotenv import load_dotenv
from langchain_anthropic import ChatAnthropic
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableLambda, RunnableParallel
from langchain_openai import ChatOpenAI

load_dotenv()

prompt = ChatPromptTemplate.from_template(
    "주어진 '{word}'와 유사한 단어 3가지를 나열해주세요. 단어만 나열합니다."
)
model = ChatOpenAI(temperature=1.0, model="gpt-5-mini")
model2 = ChatAnthropic(model="claude-sonnet-4-5-20250929")
parser = StrOutputParser()

# ① 여러 분석을 동시에 수행
analysis_chain = RunnableParallel(
    synonyms=prompt | model | parser,  # ② 유사어 분석
    synonyms2=prompt | model2 | parser,  # ② 유사어 분석
    word_count=RunnableLambda(lambda x: len(x["word"])),  # ② 단어 수 계산
    uppercase=RunnableLambda(lambda x: x["word"].upper()),  # ② 대문자로 변환
)

result = analysis_chain.invoke({"word": "interest"})
print(result)
