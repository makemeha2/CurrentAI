import random
from typing import Any, Dict

from dotenv import load_dotenv
from langchain.tools import tool
from langchain_core.messages import AIMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableLambda
from langchain_openai import ChatOpenAI

load_dotenv()


# ① Tool 정의
@tool
def rps() -> str:
    """가위바위보 중 하나를 랜덤하게 선택"""
    return random.choice(["가위", "바위", "보"])


# ② 승부 판정 로직(그대로 사용)
def judge(user_choice: str, computer_choice: str) -> str:
    user_choice = user_choice.strip()
    computer_choice = computer_choice.strip()
    if user_choice == computer_choice:
        return "무승부"
    elif (user_choice, computer_choice) in [
        ("가위", "보"),
        ("바위", "가위"),
        ("보", "바위"),
    ]:
        return "승리"
    else:
        return "패배"


# ③ LLM 준비
llm_with_tools = ChatOpenAI(temperature=0.0).bind_tools([rps])
llm_for_chat = ChatOpenAI(temperature=0.7)


# ===== 파이프라인 구성(모든 단계 | 로 연결) =====

# A) 사용자 입력 -> LLM에게 "툴 쓰라" 프롬프트 만들기
play_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "너는 가위바위보 게임 진행자야. 필요하면 제공된 도구를 사용해도 돼.",
        ),
        (
            "human",
            "가위바위보 게임: 사용자가 {user_input}를 냈습니다. rps tool을 사용해서 AI의 선택을 정하세요.",
        ),
    ]
)


# B) LLM 응답(AIMessage)에서 tool_calls를 확인하고,
#    - tool_calls가 있으면: rps 실행 결과를 사용
#    - tool_calls가 없으면: 그래도 안전하게 rps 실행(폴백)
def extract_or_run_tool(inputs: Dict[str, Any]) -> Dict[str, Any]:
    """
    inputs = {
      "user_input": "...",
      "ai_msg": AIMessage
    }
    """
    user_input = inputs["user_input"]
    ai_msg: AIMessage = inputs["ai_msg"]

    # LLM이 tool_call을 "제안"했는지 확인
    # (여기서 실제 실행은 우리가 한다)
    if getattr(ai_msg, "tool_calls", None):
        ai_choice = rps.invoke("")  # 실제 tool 실행
        tool_used = True
    else:
        # 폴백: tool_call이 없어도 게임 진행을 위해 tool 실행
        ai_choice = rps.invoke("")
        tool_used = False

    result = judge(user_input, ai_choice)

    return {
        "user_input": user_input,
        "ai_choice": ai_choice,
        "result": result,
        "tool_used": tool_used,
    }


# C) 해설 프롬프트 -> 해설 LLM
commentary_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "너는 게임 해설자야. 짧고 재밌게 2~4문장으로 해설해줘."),
        (
            "human",
            "가위바위보 결과를 해설해줘.\n"
            "- 사용자: {user_input}\n"
            "- AI: {ai_choice}\n"
            "- 결과: 사용자의 {result}\n"
            "- 참고: tool_used={tool_used}",
        ),
    ]
)


# D) 최종 출력 텍스트 만들기
def format_final_text(d: Dict[str, Any]) -> str:
    return (
        f"게임 요약: 당신({d['user_input']}) vs AI({d['ai_choice']}) => {d['result']}\n"
        f"LLM 해설: {d['commentary']}"
    )


# ---- 전체 체인을 | 로 연결 ----
# user_input(str)
#  -> {"user_input": ...}
#  -> play_prompt
#  -> llm_with_tools
#  -> {"user_input": ..., "ai_msg": AIMessage}
#  -> extract_or_run_tool
#  -> commentary_prompt
#  -> llm_for_chat
#  -> 최종 문자열
chain = (
    RunnableLambda(lambda user_input: {"user_input": user_input})
    | RunnableLambda(
        lambda d: {
            "user_input": d["user_input"], # type: ignore
            "messages": play_prompt.format_messages(**d),
        }
    )
    | RunnableLambda(
        lambda d: {
            "user_input": d["user_input"], # pyright: ignore[reportIndexIssue]
            "ai_msg": llm_with_tools.invoke(d["messages"]), # type: ignore
        }
    )
    | RunnableLambda(extract_or_run_tool)
    | RunnableLambda(
        lambda d: {**d, "messages": commentary_prompt.format_messages(**d)} # type: ignore
    )
    | RunnableLambda(
        lambda d: {**d, "commentary": llm_for_chat.invoke(d["messages"]).content} # type: ignore
    )
    | RunnableLambda(format_final_text)
)

# ===== 실행 =====
print("가위바위보! (종료: q)")
while True:
    user_input = input("\n가위/바위/보: ").strip()
    if user_input == "q":
        break
    print(chain.invoke(user_input))
