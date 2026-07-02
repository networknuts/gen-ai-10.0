from dotenv import load_dotenv
from openai import OpenAI 

# LOAD THE DOTENV DATA
load_dotenv()

# ASSIGN OPENAI A VARIABLE
client = OpenAI()

# ASK FOR USER QUERY
query = input("Human Input: ")

# MAKE THE API CALL
response = client.responses.create(
    model="gpt-5.4-mini",
    input=query
)

# PRINT THE OUTPUT
print(response.output_text)