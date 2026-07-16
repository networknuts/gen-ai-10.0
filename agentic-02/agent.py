from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, END 
from typing import TypedDict 

# SETUP THE ENVIRONMENT
load_dotenv()

llm_developer = ChatOpenAI(
    model="gpt-5.6-terra"
)

llm_qa = ChatOpenAI(
    model="gpt-5.6-sol"
)

# DEFINE THE STATE
class CodeState(TypedDict):
    user_request: str
    code: str 
    rating: int 
    retries: int 
    feedback: str 
    status: str 

# NODE 1: DEVELOPER NODE
def developer_node(state: CodeState):
    prompt = f"""
    You are a java developer.
    Write code for the following requirement of the user:
    {state['user_request']}

    If feedback is provided, improve the previous version of the code.
    Previous code:
    {state['code']}

    Feedback:
    {state['feedback']}
    """
    result = llm_developer.invoke(prompt).content.strip()
    return {
        "code": result,
        "feedback": ""
    }

# NODE 2: QA NODE
def qa_node(state: CodeState):
    prompt = f"""
    You are a senior java QA engineer.
    Evaluate the following java code for the given requirements:
    - Correctness of the code
    - Structure of the code
    - Readability of the code
    - Is the code following production best practices
    - The error handling capability of the code
    - The scalability factor of the code if required to scale in the future
    - Whether the code is using the right packages which are globally accepted

    Return the output in the following JSON format:
    {{
        "rating": integer value between 1-10,
        "feedback": string value with clear explanation of what improvements to make to the code
    }}

    Code: 
    {state['code']}
    """
    result = llm_qa.invoke(prompt).content.strip()
    return {
        "rating": int(result["rating"]),
        "feedback": result["feedback"]
    }