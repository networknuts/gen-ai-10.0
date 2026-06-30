def add_together(n1,n2):
    return(n1+n2)

def get_user_info(name,id,location):
    return {
        "user_name": name,
        "user_id": id,
        "user_location": location
    }

response = get_user_info("aryan","10","india")
print(response)