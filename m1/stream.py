from typing import Iterator
from langchain_core.messages import HumanMessage
import os
from dotenv import load_dotenv

load_dotenv()

numbers = [1, 2, 3]

def numbers_generator(numbers: list[int]) -> Iterator[int]:
    for number in numbers:
        yield number
        
try:
    for number in numbers_generator(numbers):
        # number es como se hiciera un next()
        import time
        time.sleep(1)
        print(number, end=" ", flush=True) # fluch para que se imprima inmediatamente
    
except StopIteration:
    print("No hay más números en el generador.")    
    
    
# llm = ChatOpenAI(
#     api_key=os.getenv("OPENAI_API_KEY"),
#     model="gpt-4o-mini"
# )

