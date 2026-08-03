from guardrails.hub import DetectPII
from guardrails import Guard

guard = Guard().use(
    DetectPII(pii_entities=["EMAIL_ADDRESS","PHONE_NUMBER"],on_fail="fix")
)

USER_INPUT = """
Hello, my name is aryan and my email is ARYAN@NETWORKNUTS.NET
and my phone number is 9326532664.
Please draft an email from my prespective to my employer
at INFO@NETWORKNUTS.NET asking for a 10 day PTO leave.
"""

normalized_input = USER_INPUT.lower()

try:
    result = guard.validate(normalized_input)
    print(result)
except Exception as e:
    print(f"Error: {e}")