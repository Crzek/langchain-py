from dotenv import load_dotenv

load_dotenv()

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import TokenTextSplitter
from uuid import uuid4


loader = PyPDFLoader("m3/lista_productos.pdf")
dataPDF = loader.lazy_load()  # cargar el pdf de forma lazy

# Crear una lista para almacenar el contenido por página
pages_content = []
for page in dataPDF:
    pages_content.append(page.page_content)

# Configuración del chunking
text_splitter = TokenTextSplitter(
    model_name="gpt-4",  # modelo de LLM
    chunk_size=50,  # en caracteres
    chunk_overlap=10  # contenga 5 caracteres del chunk anterior
)

# Dividir el texto en chunks y asociarlos con las páginas
chunks = []
metadatas = []
for page_number, page_content in enumerate(pages_content):
    page_chunks = text_splitter.split_text(page_content)  # dividir el texto de la página
    chunks.extend(page_chunks)  # agregar los chunks a la lista principal
    metadatas.extend([{"filename": "lista_productos.pdf", "page": page_number + 1}] * len(page_chunks))

print("chunks: ", len(chunks))
print("chunks: ", chunks[0])
print("chunks: ", chunks[1])

from chromaDB import ChromaDBManager

# instancia y creación de la base de datos
chromadb_manager = ChromaDBManager("m3/chromadb.db")  # crear la base de datos

# generar ids para cada chunk
uuids = [str(uuid4()) for _ in range(len(chunks))]  # crear una lista de ids

# metadatas = [{"filename": "lista_productos.pdf", "page": i + 1} for i in range(len(texts))]

# almacenar los chunks en la base de datos
# Esto se debe ejecutar una sola vez
# # hace la llamada a la API de OpenAI para generar los embeddings
# chromadb_manager.store(
#     texts=chunks,
#     metadatas=metadatas,
#     ids=uuids
# )
# print("----", end="\n")
# print("Almacenados en la base de datos: ", len(chunks), " chunks")
# print("primer chunk: ", chunks[0])
# print("primer metadata: ", metadatas[0])
# print("primer uuid: ", uuids[0])
# # --BUSQUEDA--
# # para encontrar por metadata
# chromadb_manager.find(
#     metadata={"filename": "lista_productos.pdf"}
# )

# # para eliminar documentos
# chromadb_manager.drop(
#     metadata={"filename": "lista_productos.pdf"}
# )

# --HACER CONSULTA--
query = "Que productos tienes?"
result:list = chromadb_manager.query(
    query=query,
    metadata={"filename": "lista_productos.pdf"},
)

# query = [Document(id='8ff3993e-56ef-4451-89e9-c5bfb02749a6', metadata={'filename': 'lista_productos.pdf', 'page': 1}, page_content='CATÁLOGO DE PRODUCTOS TECNOLÓGICOS\nNombre del producto:'),...]
# convertimos el resultado a un string con saltos de linea
print("Se ha encontrado:", len(result), " resultados")
context = "\n".join([doc.page_content for doc in result])

# CREAR TemPLATE
from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI

prompt_template = PromptTemplate.from_template("""
    Eres un asistente de ventas de una tienda de tecnología.
    Debes responder en base a la información del 'Context'
    
    **Context**:
    {context}
    
    **Pregunta**:
    {query}
    """)

llm = ChatOpenAI(model="gpt-4.1-nano", max_completion_tokens=2000)
chain = prompt_template | llm
chain_response = chain.invoke({
    "context": context,
    "query": query
})
print("----",end="\n")
print("Context: ", context)

print("----",end="\n")
print("Chain response: ", chain_response.content)