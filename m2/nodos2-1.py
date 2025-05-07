from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field
from langgraph.graph import StateGraph # Grafo basado en (stados)
from langgraph.graph import START, END

load_dotenv()

# schema de respuesta
class AgentState(BaseModel):
    user_message: str =  ""
    agent_message: str = ""
    greeting: bool = False
    
# Nodo 1: leer el estado
def greeting_node(agent_state: AgentState) -> AgentState:
    """leyendo estado y modificando el estado"""
    if "hola" in agent_state.user_message.lower():
        agent_state.greeting = True
    else:
        agent_state.greeting = False
    return agent_state 

# Nodo 2: leer el estado
def response_node(agent_state: AgentState) -> AgentState:
    """leyendo estado y modificando el estado"""
    if agent_state.greeting:
        agent_state.agent_message = "Hola, ¿cómo estás?"
    else:
        agent_state.agent_message = "No entiendo"
    return agent_state

# Crear el grafo
my_graph = StateGraph(AgentState)
# Agregar los nodos al grafo
my_graph.add_node(greeting_node)
my_graph.add_node(response_node)  

# Conectar los nodos (flujo de datos) flechas
my_graph.add_edge(START, "greeting_node")
my_graph.add_edge("greeting_node", "response_node")
my_graph.add_edge("response_node", END)

# copilar el grafo
compile_graph = my_graph.compile()

# inicializar el agente y se pasa al grafo
initial_state = AgentState(user_message="hey")
grph_res = compile_graph.invoke(initial_state)
print("Respuesta: ", grph_res["agent_message"])