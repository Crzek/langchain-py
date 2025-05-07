from langchain_openai import ChatOpenAI

from dotenv import load_dotenv

load_dotenv()

msg="Cual es la velocidad de la luz?"

llm = ChatOpenAI(model="gpt-4.1-nano", max_completion_tokens=800)
for chunk in llm.stream(msg):
    print(chunk.content, end="", flush=True)
    # print(chunk.content, end="")
print(llm.invoke(msg))
