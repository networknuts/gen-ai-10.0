import redis
import uuid

# SETUP THE REDIS CONNECTION
redis_client = redis.Redis(
    host="localhost",
    port=6379,
    decode_responses=True
)

# GENERATE PAYLOAD AND PUSH TO REDIS
def push_payload(query):
    job_id = str(uuid.uuid4())
    payload = {
        "job_id": job_id,
        "query": query
    }
    queue_name = "rag:requests" # application_name:queue_purpose
    redis_client.rpush(queue_name,str(payload))
    return job_id

# ASK FOR USER INPUT
query = input("Human Question: ")

# SEND QUERY TO QUEUE VIA PUSH_PAYLOAD FUNCTION
job = push_payload(query)
print("Query sent to redis successfully.")
print(job)