import redis
import ast
from dotenv import load_dotenv
from openai import OpenAI 
from langchain_qdrant import QdrantVectorStore
from langchain_openai import OpenAIEmbeddings

# SETUP THE AI ENVIRONMENT
load_dotenv()
client = OpenAI()

VECTOR_DB_URL = "http://localhost:6333"
COLLECTION_NAME = "product_documentation"
EMBEDDINGS = OpenAIEmbeddings(
    model="text-embedding-3-large"
)

qdrant = QdrantVectorStore.from_existing_collection(
    embedding=EMBEDDINGS,
    collection_name=COLLECTION_NAME,
    url=VECTOR_DB_URL
)

# SETUP THE REDIS CONNECTION
queue_name = "rag:requests"
redis_client = redis.Redis(
    host="localhost",
    port=6379,
    decode_responses=True
)

# PULL DATA OUT OF QUEUE
print("\nWORKER STARTED, WAITING FOR PAYLOAD\n")

while True:
    queue_name, raw_payload = redis_client.blpop(queue_name)
    payload = ast.literal_eval(raw_payload)
    job_id = payload['job_id']
    query = payload['query']
    print(f"Processing Query: {job_id}")

    # AI RAG CODE
    search_results = qdrant.similarity_search(query)
    context = []
    for chunk in search_results:
        chunk_block = f"""
        Page Content:
        {chunk.page_content}
        Page Number:
        {chunk.metadata.get("page_label","N/A")}
        """
        context.append(chunk_block)
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
    response = client.responses.create(
    model="gpt-5.4-mini",
    input=query,
    instructions=SYSTEM_PROMPT
    )
    answer = response.output_text
    redis_client.set(
        f"rag:response:{job_id}",
        answer,
        ex=86400
    )
    print(f"Job {job_id} completed successfully!")