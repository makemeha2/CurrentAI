import os

import anthropic
import rich
from click import prompt
from dotenv import load_dotenv

load_dotenv()

api_key = os.environ.get("ANTHROPIC_API_KEY")
client = anthropic.Anthropic(api_key=api_key)

prompt = "anthropic 발음은 앤쓰로픽이 맞나요? 앤트로픽이 맞나요?"  # noqa: F811
with client.messages.stream(
    max_tokens=512,
    messages=[{"role": "user", "content": prompt}],
    model="claude-3-5-haiku-20241022",
) as stream:
    for event in stream:
        if event.type == "text" :
            print(event.text, end="", flush=True)
    print()

    rich.print(stream.get_final_message())
