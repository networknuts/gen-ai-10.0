import re 

EMAIL_DATA = """
john <john@networknuts.net>
jane <jane@networknuts.net>
arthur <arthur@networknuts.net>
thomas <thomas@networknuts.net>
chris <chris@networknuts.net>
bobbi <bobbi@networknuts.net>
"""

# SIMPLE STRING SEARCHING
result_1 = re.search(r"[r,b]obb[i,y]",EMAIL_DATA)

# MULTIPLE LETTERS MISSING IN A STRING
result_2 = re.search(r"chr[a-z]{2}",EMAIL_DATA)

# UNKOWN NUMBER OF LETTERS MISSING IN A STRING
result_3 = re.search(r"art[a-z]+",EMAIL_DATA)

# RE FOR AN EMAIL ADDRESS
result_4 = re.findall(r"[a-zA-Z0-9_]+@[a-zA-Z0-9_]+\.[a-zA-Z0-9_]+",EMAIL_DATA)
print(result_4)