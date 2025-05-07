from dotenv import load_dotenv

load_dotenv()

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import TokenTextSplitter


loader = PyPDFLoader("m3/lista_productos.pdf")
dataPDF = loader.lazy_load() # cargar el pdf de forma lazy

text = ""
for page in dataPDF:
    text += page.page_content + "\n"
    # print("page: ", page.page_content)

# Configuración del chunking
text_splitter = TokenTextSplitter(
    model_name="gpt-4", # modelo de LLM
    chunk_size=20, # en caracteres
    chunk_overlap=10  # contenga 5 caracteres del chunk anterior
)

texts:list = text_splitter.split_text(text) # separar el texto en chunks
print("chunks: ", len(texts))
print("chunks: ", texts[0])
print("chunks: ", texts[1])