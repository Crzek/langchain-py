from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from pydantic import BaseModel
from langchain_core.prompts import PromptTemplate

load_dotenv()

class Answer(BaseModel):
    number_of_words: int

# Crear un esquema de respuesta
prompt_template = PromptTemplate.from_template("""
    Te voy ha dar un texto y quiero que me digas cuantas palabras tiene.
    texto: {text}
""")

# Crear el modelo LLM
llm = ChatOpenAI(model="gpt-4.1-nano")

# LLM con salida estructurada
llm_structured = llm.with_structured_output(Answer)

# Crear la cadena que conecta el prompt_template con el llm_structured
chain = prompt_template | llm_structured

# Invocar la cadena con los datos de entrada
result = chain.invoke({"text": "hola mundo"})
print("Answer: ", result)# Answer:  number_of_words=2