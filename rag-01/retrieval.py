from dotenv import load_dotenv
from openai import OpenAI 
from langchain_qdrant import QdrantVectorStore
from langchain_openai import OpenAIEmbeddings

# SETUP THE ENVIRONMENT
load_dotenv()
client = OpenAI()

VECTOR_DB_URL = "http://localhost:6333"
COLLECTION_NAME = "product_documentation"
EMBEDDINGS = OpenAIEmbeddings(
    model="text-embedding-3-large"
)

# STEP 1: CONNECT TO THE VECTOR DATABASE
qdrant = QdrantVectorStore.from_existing_collection(
    embedding=EMBEDDINGS,
    collection_name=COLLECTION_NAME,
    url=VECTOR_DB_URL
)

# STEP 2: ASK FOR USER QUERY
human_query = input("Human Query: ")

# STEP 3: PERFORM SIMILARITY SEARCH
search_results = qdrant.similarity_search(human_query)

# STEP 4: CREATE CONTEXT FROM CHUNKS

context = []

for chunk in search_results:
    chunk_block = f"""
    Page Content:
    {chunk.page_content}
    Page Number:
    {chunk.metadata.get("page_label","N/A")}
    """
    context.append(chunk_block)


# STEP 5: RAG SYSTEM PROMPT
SYSTEM_PROMPT = f"""
You are a RAG AI Assistant.
You have been provided content extracted from a PDF document.
Each section includes:
- The page content
- The page number

Answer the user's query using ONLY this provided information.
If the answer is available:
- Respond clearly from the data you have received
- Mention the relevant page number(s) from where the data was extracted

If the answer is not available:
- State to the user that the answer is not in your knowledge base

Context:
{context}
"""

# STEP 6: GENERATE THE LLM RESPONSE
response = client.responses.create(
    model="gpt-5.4-mini",
    input=human_query,
    instructions=SYSTEM_PROMPT
)

# STEP 7: PRINT THE RESPONSE
print(response.output_text)