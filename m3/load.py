from dotenv import load_dotenv

load_dotenv()

from langchain_openai import ChatOpenAI
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.document_loaders import  Docx2txtLoader
from langchain_community.document_loaders import TextLoader
from langchain_community.document_loaders import CSVLoader




loader = PyPDFLoader("m3/myCv.pdf")
# dataPDF = loader.load() # cargar el pdf
dataPDF = loader.lazy_load() # cargar el pdf de forma lazy
# si tubiera paguinas
for page in dataPDF:
    print("page: ", page.page_content)
    
    
doc_loader = Docx2txtLoader("m3/myCv.docx")
doc_loader.lazy_load()

for page in doc_loader:
    print("page: ", page.page_content)