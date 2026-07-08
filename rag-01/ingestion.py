from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_qdrant import QdrantVectorStore
from dotenv import load_dotenv

# SETUP THE ENVIRONMENT
load_dotenv()
PDF_PATH = "large_data.pdf"
VECTOR_DB_URL = "http://localhost:6333"
COLLECTION_NAME = "product_documentation"

# STEP 1: LOAD THE PDF INTO TEXT
loader = PyPDFLoader(PDF_PATH)
pdf_text_data = loader.load()
print("PDF LOADED SUCCESSFULLY")

# STEP 2: CREATE A CHUNKING STRATEGY
text_splitter = RecursiveCharacterTextSplitter(chunk_size=100, chunk_overlap=0)
chunked_data = text_splitter.split_documents(pdf_text_data)
print("PDF CHUNKED SUCCESSFULLY")

# STEP 3: CHOOSING AN EMBEDDING MODEL
embeddings = OpenAIEmbeddings(
    model="text-embedding-3-large"
)

# STEP 4: STORE CHUNKS INTO VECTOR DATABASE
qdrant = QdrantVectorStore.from_documents(
    chunked_data,
    embeddings,
    url=VECTOR_DB_URL,
    prefer_grpc=False,
    collection_name=COLLECTION_NAME
)
print("INGESTION COMPLETED.")