from typing import Literal
from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field
from langgraph.graph import StateGraph # Grafo basado en (stados)
from langgraph.graph import START, END
from langchain_core.prompts import PromptTemplate

load_dotenv()

# schema de respuesta -> Representa el estado del agente
class Languageoutput(BaseModel):
    language: Literal["es", "en"]
    
class AgentState(BaseModel):
    user_message: str =  ""
    agent_message: str = ""
    greeting: bool = False
    language: Languageoutput = None

class GreetingOutput(BaseModel):
    greeting:bool
    
    
# Nodo 1: leer el estado
def greeting_node(agent_state: AgentState) -> AgentState:
    prompt_template = PromptTemplate.from_template("""
    Tu respuesta debe ser true si el usuario esta saludando,
    false en caso contrario.
    El mensaje del usuario es: {text}
    """)
    
    llm = ChatOpenAI(model="gpt-4.1-nano")
    llm_structured = llm.with_structured_output(GreetingOutput)
    
    chain = prompt_template | llm_structured
    chain_res = chain.invoke({"text": agent_state.user_message})
    agent_state.greeting = chain_res.greeting
    return agent_state
    

# Nodo 2: leer el estado
def response_node(agent_state: AgentState) -> AgentState:
    
    if agent_state.greeting:
        agent_state.agent_message = "Hola, ¿cómo estás?"
    else:
        llm = ChatOpenAI(model="gpt-4.1-nano")
        llm_res = llm.invoke(agent_state.user_message)
        agent_state.agent_message = llm_res.content
    return agent_state

#nodes de idiomas
def spanish_response_node(agent_state: AgentState) -> AgentState:
    agent_state.agent_message += "\n idioma: español"
    return agent_state

def english_response_node(agent_state: AgentState) -> AgentState:
    agent_state.agent_message += "\n idioma: ingles"
    return agent_state

# Condicional (elige que nodo ejecutar (spanicsh o ingles))
def language_node(agent_state: AgentState) -> Literal["spanish_response_node", "english_response_node"]:
    prompt_template = PromptTemplate.from_template("""
    En que idioma esta el mensaje del usuario?
    Responde con 'es' para español o 'en' para ingles, es formato json.
    El mensaje del usuario: {text}
    """)
    
    llm = ChatOpenAI(model="gpt-4.1-nano")
    llm_structured = llm.with_structured_output(Languageoutput)
    
    chain = prompt_template | llm_structured
    chain_res = chain.invoke({"text": agent_state.user_message})
    
    # setteas el idioma en el estado
    agent_state.language = chain_res.language
    
    if agent_state.language == "es":
        return "spanish_response_node"
    elif agent_state.language == "en":
        return "english_response_node"
    else:
        raise ValueError("Invalid language response")


# Crear el grafo
my_graph = StateGraph(AgentState)
# Agregar los nodos al grafo
my_graph.add_node(greeting_node)
my_graph.add_node(response_node)  
my_graph.add_node(english_response_node)
my_graph.add_node(spanish_response_node)

# Conectar los nodos (flujo de datos) flechas
my_graph.add_edge(START, "greeting_node")
my_graph.add_edge("greeting_node", "response_node")

# Condicional if else
my_graph.add_conditional_edges(
    "response_node", # inicio del condicional
    language_node, # nodo que decide el flujo siguiente
)
my_graph.add_edge("spanish_response_node", END)
my_graph.add_edge("english_response_node", END)


# copilar el grafo
compile_graph = my_graph.compile()

# inicializar el agente y se pasa al grafo
# initial_state = AgentState(user_message="hey")
# grph_res = compile_graph.invoke(initial_state)
# print("Respuesta: ", grph_res["agent_message"])