import redis
import time

# SETUP THE REDIS CONNECTION
redis_client = redis.Redis(
    host="localhost",
    port=6379,
    decode_responses=True
)

job_id = input("Enter your Job ID: ")

while True:
    result = redis_client.get(f"rag:response:{job_id}")
    if result:
        print(f"\n{result}\n")
        break
    else:
        print("Retrying in 5 seconds")
        time.sleep(5)