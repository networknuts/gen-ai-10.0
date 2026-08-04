import redis
from openai import OpenAI 
from dotenv import load_dotenv
import uuid 
from qdrant_client import QdrantClient, models
from qdrant_client.models import PointStruct
import hashlib

# SETUP THE ENVIRONMENT
load_dotenv()
client = OpenAI()

# SETUP REDIS CONNECTION
redis_client = redis.Redis(
    host="localhost",
    port=6379,
    decode_responses=True
)

# SETUP THE QDRANT CONNECTION
qdrant = QdrantClient(url="http://localhost:6333")
COLLECTION = "cache"

# STEP 1: HASHING STRATEGY
def convert_hash(prompt: str):
    normalized = prompt.strip().lower()
    hashed = hashlib.sha256(normalized.encode()).hexdigest()
    return f"cache:{hashed}"

# STEP 2: GENERATE THE LLM RESPONSE
def ask_llm(prompt: str):
    response = client.responses.create(
        model="gpt-5.4-mini",
        input=prompt
    )
    return response.output_text

# STEP 3: EMBEDDING MODEL STRATEGY
def get_embedding(text):
    response = client.embeddings.create(
        input=text,
        model="text-embedding-3-small"
    )
    return response.data[0].embedding

# STEP 4: INITIALIZE THE VECTOR DATABASE
def init_collection():
    try:
        qdrant.get_collection(COLLECTION)
    except:
        qdrant.create_collection(
            collection_name=COLLECTION,
            vectors_config=models.VectorParams(size=1536,distance=models.Distance.COSINE)
        )

# STEP 4: SEARCH THE COLLECTION FOR SEMANTIC RESULTS
def search_cache(embedding):
    result = qdrant.query_points(
        collection_name=COLLECTION,
        query=embedding,
        limit=1
    )
    if len(result.points) == 0:
        return None
    point = result.points[0]
    if point.score > 0.9:
        return point.payload["answer"]
    return None 

# STEP 4: SAVE ANSWER TO VECTOR DB
def save_cache(prompt,embedding,answer):
    qdrant.upsert(
        collection_name=COLLECTION,
        points=[
            PointStruct(
                id=str(uuid.uuid4()),
                vector=embedding,
                payload={
                    "prompt": prompt,
                    "answer": answer
                }
            )
        ]
    )

# MAIN LOGIC
def get_answer(prompt):
    key = convert_hash(prompt)
    cached_output = redis_client.get(key)
    if cached_output:
        print("FOUND RESPONSE IN REDIS CACHE")
        return cached_output
    else:
        emb = get_embedding(prompt)
        init_collection()
        semantic_result = search_cache(emb)
        if semantic_result:
            print("FOUND RESPONSE IN VECTOR DB CACHE")
            redis_client.set(key,semantic_result)
            return semantic_result
        else:
            print("INVOKING LLM CALL")
            answer = ask_llm(prompt)
            # SAVE TO REDIS
            redis_client.set(key,answer)
            # SAVE TO QDRANT
            save_cache(prompt,emb,answer)
            return answer 

query = input("Human Query: ")
print("\nAI RESPONSE\n")
print(get_answer(query))