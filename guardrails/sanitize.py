import re

USER_INPUT = """
Hello, my name is aryan and my email is ARYAN@NETWORKNUTS.NET
Please draft an email from my prespective to my employer
at INFO@NETWORKNUTS.NET asking for a 10 day PTO leave.
"""

normalized_input = USER_INPUT.lower()

result = re.findall(r"[a-zA-Z0-9_]+@[a-zA-Z0-9_]+\.[a-zA-Z0-9_]+",normalized_input)
refined_result = re.findall(r"\w+@\w+\.\w+",normalized_input)

sanitized_input = re.sub(r"\w+@\w+\.\w+","<REDACTED_EMAIL>",normalized_input)
print(sanitized_input)