import os
from dotenv import load_dotenv
import anthropic

load_dotenv()

api_key = os.environ.get("OPENAI_API_KEY")
client = anthropic.Anthropic()

conversation = []

conversation.append({"role" : "user", "content" : "안녕, 나는 소영이야."})

response = client.messages.create(
    model = "claude-3-5-haiku-latest",
    max_tokens=1000,
    messages=conversation
)

assistant_message = response.content[0].text
print(assistant_message)
conversation.append({"role" : "assistant", "content" : assistant_message})

conversation.append({"role" : "user", "content" : "내 이름이 뭐라고 했더라?"})

response = client.messages.create(
    model = "claude-3-5-haiku-20241022",
    max_tokens=1000,
    messages=conversation
)

print(response.content[0].text)

# if __name__ == "__main__":
#     prompt = """
#         https://platform.openai.com/docs/api-reference/responses/create 
#         를 읽어서 Responses API에 대해 요약 정리해주세요. 
#     """

#     output = get_responses(prompt)
#     print(output)

