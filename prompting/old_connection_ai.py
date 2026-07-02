from dotenv import load_dotenv
from openai import OpenAI 

# LOAD THE .ENV FILE
load_dotenv()

# SET THE OPENAI VARIABLE
client = OpenAI()

response = client.chat.completions.create(
    model="gpt-5.4-mini",
    messages=[
        {"role":"user","content":"what is the capital of India?"}
    ]
)
print(response)