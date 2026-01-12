from agents import Agent, Runner
from dotenv import load_dotenv

load_dotenv()

hello_agent = Agent(
    name="HelloAgent",
    instructions="당신은 helloAgent입니다. 당신의 임무는 '안녕하세요'라고 인사하는 겁니다. 그 외에 인사로 사용할 수 있는 다른 말을 곁들일 수 있습니다."
)

result = Runner.run_sync(hello_agent, "나는 안녕하지 못해. 그래도 넌 안녕하세요? 라고 대답할꺼야?.")
print(result.final_output)