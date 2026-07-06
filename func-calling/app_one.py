import requests
from dotenv import load_dotenv
import os
from openai import OpenAI 
import json

# SETUP THE ENVIRONMENT
load_dotenv()
client = OpenAI()

f = open("weather_func_description.txt")
weather_func_description = f.read()
f.close()

# CREATE MY WEATHER CALLING FUNCTION
def get_weather(zipcode):
    countrycode = "in"
    apikey = os.getenv("WEATHER_API_KEY")
    url = f"https://api.openweathermap.org/data/2.5/weather?zip={zipcode},{countrycode}&appid={apikey}"
    result = requests.get(url)
    response = result.json()
    return response


# DEFINE THE SCHEMA
openai_tools = [
    {
        "type": "function",
        "name": "get_weather",
        "description": weather_func_description,
        "parameters": {
            "type": "object",
            "properties": {
                "zipcode": {
                    "type": "string",
                    "description": "The zipcode of the location to get the weather data of."
                },
            },
            "required": ["zipcode"]
        }
    }
]

# ASK FOR USER QUERY
user_query = input("HUMAN: ")

# MAKE THE LLM CALL
response = client.responses.create(
    model="gpt-5.4-mini",
    input=user_query,
    tools=openai_tools
)

function_output = []

for item in response.output:
    if item.type == "function_call":
        args = json.loads(item.arguments) #convert str to dict
        if item.name == "get_weather":
            result = get_weather(args['zipcode'])
            print("RAW FUNCTION OUTPUT")
            print(result)
            print("----------------")
        else:
            result = "unknown function called"

        function_output.append({
            "type": "function_call_output",
            "call_id": item.call_id,
            "output": json.dumps({"result": result}) #dict to str
        })

# SECOND LLM CALL
final_response = client.responses.create(
    model="gpt-5.4-mini",
    input=function_output,
    previous_response_id=response.id
)

print("\nAI SUMMARIZED OUTPUT\n")
print(final_response.output_text)