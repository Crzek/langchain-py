from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import CommaSeparatedListOutputParser

load_dotenv()

llm = ChatOpenAI()
res_llm = llm.invoke("""
    dame una lista de 3 frutas separadas por comas 
    ejemplo: manzana, naranja, banana
    """)

parser = CommaSeparatedListOutputParser()

parser_result = parser.invoke(res_llm.content)

print(parser_result)# ['manzana', 'naranja', 'banana']

