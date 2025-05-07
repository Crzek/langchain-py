from dotenv import load_dotenv

load_dotenv()

from langchain_openai import ChatOpenAI
from langchain_community.document_loaders import PyPDFLoader

# Splitters permite realizar los chunking de los documentos
# from langchain_text_splitters import CharacterTextSplitter
# Podemos usar varios tipos de splitters
from langchain_text_splitters import RecursiveCharacterTextSplitter


loader = PyPDFLoader("m3/lista_productos.pdf")
dataPDF = loader.lazy_load() # cargar el pdf de forma lazy

text = ""
for page in dataPDF:
    text += page.page_content + "\n"
    # print("page: ", page.page_content)

# Configuración del chunking
text_splitter = RecursiveCharacterTextSplitter(
    separators=["\n\n", "\n", ".", " ", ","], # VARIOS SEPARADORES
    chunk_size=1000, # en caracteres
    chunk_overlap=200  # contenga 200 caracteres del chunk anterior
    # que se repita info en el chunk siguiente
)

texts:list = text_splitter.split_text(text) # separar el texto en chunks
print("chunks: ", len(texts))
print("chunks: ", texts[0])
print("chunks: ", texts[1])