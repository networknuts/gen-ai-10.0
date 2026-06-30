import requests

# VARIABLES REQUIRED FOR THE URL
API_KEY = ""
ZIP_CODE = input("Enter your zipcode: ")
COUNTRY_CODE = "in"

#FORMATION OF THE URL
WEATHER_URL = f"https://api.openweathermap.org/data/2.5/weather?zip={ZIP_CODE},{COUNTRY_CODE}&appid={API_KEY}"

# MAKING THE CONNECTION TO THE URL
response = requests.get(WEATHER_URL)

# PRINTING URL RESPONSE
print(response.json())