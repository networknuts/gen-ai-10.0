from dotenv import load_dotenv
from openai import OpenAI 

# LOAD THE DOTENV DATA
load_dotenv()

# ASSIGN OPENAI A VARIABLE
client = OpenAI()

# LOAD THE SYSTEM PROMPT
f = open("cot.txt","r")
SYSTEM_PROMPT = f.read()
f.close()

# ASK FOR USER QUERY
user_query = input("Human Question: ")

# API CALL
response = client.responses.create(
    model="gpt-5.4-mini",
    reasoning={"effort": "high"},
    input=user_query,
    instructions=SYSTEM_PROMPT
)

print("AI RESPONSE\n")
print(response.output_text)