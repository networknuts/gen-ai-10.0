from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, END 
from typing import TypedDict 

# SETUP THE ENVIRONMENT
load_dotenv()

llm = ChatOpenAI(
    model="gpt-5.4-mini"
)

# DEFINE THE STATE
class SupportState(TypedDict):
    user_query: str 
    intent: str 
    response: str 

# NODE 1: INTENT CLASSIFIER NODE
def classify_intent(state: SupportState):
    prompt = f"""
    Classify the user query into one of these categories:
    - password_reset
    - order_tracking
    - refund_request

    Only return the category name.
    User Query: {state['user_query']}
    """
    result = llm.invoke(prompt)
    return {
        "intent": result.content.strip().lower()
    }