page_number = input("Enter page number: ")
api_key = input("Enter API KEY: ")

internal_url = f"https://networknuts.net/{page_number}/apikey={api_key}"
print(internal_url)