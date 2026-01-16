from typing import Annotated, Any

from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages
from pydantic import BaseModel, ConfigDict


class NewsState(BaseModel) :
    """뉴스 처리 상태를 관리하는 데이터 모델"""
    # pydantic이 모르는 타입을 허용
    model_config = ConfigDict(arbitrary_types_allowed=True)
    
    messages: Annotated[list[BaseMessage], add_messages] = []
    raw_news: list[dict[str, Any]] = []
    summarized_news: list[dict[str, Any]] = []

    categorized_news: dict[str, list[dict[str, Any]]] = {}
    final_report: str = ""
    error_log: list[str] = []


