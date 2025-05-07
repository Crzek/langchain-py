from dotenv import load_dotenv

# interceptar el input y output de la LLM
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field

load_dotenv()

# Crear Schema de Respuesta
class AnswerwithJustification(BaseModel):
    """Respuesta con justificación""" # esto es para el LLM
    answer: str = Field(description="La respuesta a la pregunta")
    justification: str = Field(description="La justificación que respalda la respuesta")

#LLM
llm = ChatOpenAI(model="gpt-4.1-nano")
# LLM con salida estructurada
llm_structured = llm.with_structured_output(AnswerwithJustification)
res_llm = llm_structured.invoke("Cual es la velocidad de la luz?")

# acceder a los atributos de la respuesta
print("Answer: ",res_llm.answer)
# Answer:  La velocidad de la luz en el vacío es aproximadamente 
# 299,792 kilómetros por segundo.
print("Justification: ",res_llm.justification)
# Justification:  Esta velocidad es una constante universal, 
# comúnmente redondeada a 300,000 km/s para simplificación, 
# y ha sido determinada a través de experimentos y mediciones precisas 
# en física. Es importante en la teoría de la relatividad 
# y en la comprensión de la naturaleza del espacio y el tiempo.



