# from langchain import OpenAIEmbeddings
import numpy as np
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings

load_dotenv()

embeddings = OpenAIEmbeddings(model="text-embedding-3-large")

# 단어들을 임베딩으로 변환
words = ["강아지", "고양이", "자동차", "비행기"]
word_embeddings = embeddings.embed_documents(words)

# 쿼리 임베딩 생성
query = "동물"
query_embeddings = embeddings.embed_query(query)

# 코사인 유사도 계산 함수
def cosine_similarity(vec1, vec2):
    dot_product = np.dot(vec1, vec2)
    norm_vec1 = np.linalg.norm(vec1)
    norm_vec2 = np.linalg.norm(vec2)
    return dot_product / (norm_vec1 * norm_vec2 + 1e-9)     # 0 나누기 오류 방지 지수 삽입

print(f"'{query}'에 대한 유사도: ")
for word, embedding in zip(words, word_embeddings):
    similarity = cosine_similarity(query_embeddings, embedding)
    print(f"{word} : {similarity:.3f}")