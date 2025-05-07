from langchain_core.prompts import PromptTemplate, ChatPromptTemplate
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()

template = ChatPromptTemplate.from_messages([
    ("system", "Eres un traductor de palabras"),
    ("user", "traducir al idioma: {language}"),
    ("user", "palabra: {text}"),
])

prompt = template.invoke({
    "language": "ingles",
    "text": "soy una persona curiosa"
})



# # Crear un template de prompt
# prompt_template = PromptTemplate.from_template("""
# Tarducir al Idioma: {language}
# la siguiente frase: {text}
# """)

# # se le pasa un diccionario
# prompt = prompt_template.invoke({
#     "language": "ingles",
#     "text": "soy una persona curiosa"
# })

# Crear un modelo de lenguaje
# Se le pasa el prompt como un mensaje
llm = ChatOpenAI()
res = llm.invoke(prompt)
print(res.content)