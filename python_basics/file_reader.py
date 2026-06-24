# The user shall provide a file path
# and our code is responsible for 
# printing the content of that file.

file_path = input("Enter file path to read: ")

f = open(file_path,"r")

for item in f.readlines():
    print(item.strip())

f.close()