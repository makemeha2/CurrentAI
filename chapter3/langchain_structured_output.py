from typing import cast

from dotenv import load_dotenv
from langchain_chat_model import init_chat_model
from pydantic import BaseModel, Field

load_dotenv()

llm = init_chat_model("gpt-5-mini", model_provider="openai")

class MovieReview(BaseModel):
    title: str = Field(description="영화제목")
    rating: float = Field(description="10점 만점 평점 (예 : 7.5)")
    review: str = Field(description="한글 리뷰 (3~4문장)")

structured_llm = llm.with_structured_output(MovieReview)

result: MovieReview = cast(MovieReview, structured_llm.invoke("영화 '기생충'에 대한 리뷰를 작성해주세요."))

print(result.title)
print(result.rating)
print(result.review)
