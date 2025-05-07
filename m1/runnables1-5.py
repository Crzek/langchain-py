from typing import Iterator
# from langchain_openai import ChatOpenAI
# from langchain_core.messages import HumanMessage, SytemMessage
from langchain_core.runnables import Runnable
from dotenv import load_dotenv

load_dotenv()

class Textinverter (Runnable):
    def invoke (self, text_input:str) -> str:
        return text_input[::-1]
    
    def stream(self, text_input:str) -> Iterator[str]:
        text_inverter = text_input[::-1]
        for char in text_inverter:
            yield char
        
text_runnable = Textinverter()
print(text_runnable.invoke("Hola mundo"))

for char in text_runnable.stream("Hola mundo"):
    import time
    time.sleep(0.1)
    print(char, end="", flush=True) # fluch para que se imprima inmediatamente
