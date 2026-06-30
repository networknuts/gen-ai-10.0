from dotenv import load_dotenv
import os
import requests
import json

# LOAD THE .ENV FILE
load_dotenv()

# GET THE OPENAI API KEY FROM THE .ENV FILE
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# SET THE OPENAI URL FROM THE DOCUMENTATION
OPENAI_URL = "https://api.openai.com/v1/responses"

# CREATE HEADERS AS PER DOCUMENTATION
HEADERS = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {OPENAI_API_KEY}"
}

# ASK FOR USER QUERY
user_question = input("Enter Your Question: ")

# SET THE DATA
DATA = {
    "model": "gpt-5.5",
    "input": user_question
}

# MAKING THE REQUEST
response = requests.post(OPENAI_URL,headers=HEADERS,data=json.dumps(DATA))

print(response.json())