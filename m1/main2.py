from langchain_anthropic import ChatAnthropic
from langchain_core.messages import HumanMessage, SytemMessage

from dotenv import load_dotenv

import os

load_dotenv()

msg = [
    SytemMessage(
        content="Eres un experto en IA y programación, por favor responde a la siguiente pregunta de manera clara y concisa."
    ),
    HumanMessage(
        content="que es Langchain?"
    )
]

llm = ChatAnthropic(
    api_key=os.getenv("ANTHROPIC_API_KEY"),
    model="claude-3-haiku-20240307"
    )

llm_response = llm.invoke(msg)
print(llm_response.content)
