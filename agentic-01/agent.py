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

# NODE 2: PASSWORD RESET NODE
def handle_password(state: SupportState):
    return {
        "response": "An email has been sent to you to change your password."
    }

# NODE 3: ORDER TRACKING NODE
def handle_order(state: SupportState):
    return {
        "response": "Please click on my orders in your profile to track a order."
    }

# NODE 4: REFUND NODE
def handle_refund(state: SupportState):
    return {
        "response": "Your refund request has been initiated."
    }

# ROUTER FUNCTION
def route_intent(state: SupportState):
    if state["intent"] == "password_reset":
        return "password_node"
    elif state["intent"] == "order_tracking":
        return "order_node"
    elif state["intent"] == "refund_request":
        return "refund_node"
    else:
        return END

# COMPILING THE GRAPH

graph = StateGraph(SupportState)

# DECLARED YOUR NODES

graph.add_node("classifier_node",classify_intent)
graph.add_node("password_node",handle_password)
graph.add_node("order_node",handle_order)
graph.add_node("refund_node",handle_refund)

graph.set_entry_point("classifier_node")
graph.add_conditional_edges("classifier_node",route_intent)
graph.add_edge("password_node",END)
graph.add_edge("order_node",END)
graph.add_edge("refund_node",END)

app = graph.compile()

# EXECUTE THE GRAPH
user_input = input("CUSTOMER QUERY: ")

result = app.invoke({
    "user_query": user_input,
    "intent": "",
    "response": ""
})

print("INTENT:\n")
print(result["intent"])
print("RESPONSE:\n")
print(result["response"])