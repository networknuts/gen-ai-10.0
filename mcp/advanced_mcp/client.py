from mcp import ClientSession
from mcp.client.streamable_http import streamable_http_client
from langgraph.graph import StateGraph, START, END
from openai import OpenAI
from dotenv import load_dotenv
from typing import TypedDict
import asyncio


load_dotenv()

client = OpenAI()
MODEL = "gpt-5.4-mini"


# =====================================================
# STATE
# =====================================================

class SupportState(TypedDict):
    customer_id: int
    question: str
    intent: str
    order_data: str
    answer: str


# =====================================================
# HELPER
# =====================================================

def get_text(contents):
    return "\n".join(
        content.text
        for content in contents
        if hasattr(content, "text")
    )


# =====================================================
# CREATE GRAPH
# =====================================================

def create_graph(session):

    # -------------------------------------------------
    # NODE 1: CLASSIFY QUESTION
    # -------------------------------------------------

    def classify_intent(state: SupportState):
        response = client.responses.create(
            model=MODEL,
            input=f"""
Classify this customer-support question.

Categories:

order_status
refund

Return only the category name.

Question:
{state["question"]}
"""
        )

        return {
            "intent": response.output_text.strip().lower()
        }

    # -------------------------------------------------
    # NODE 2: GET ORDER DATA
    # -------------------------------------------------

    async def get_order(state: SupportState):
        result = await session.call_tool(
            "get_order_data",
            {
                "customer_id": state["customer_id"]
            }
        )

        return {
            "order_data": get_text(result.content)
        }

    # -------------------------------------------------
    # NODE 3: ANSWER ORDER QUESTION
    # -------------------------------------------------

    def answer_order_question(state: SupportState):
        response = client.responses.create(
            model=MODEL,
            input=f"""
You are a customer-support assistant.

Answer the customer's question using the supplied order data.

Customer question:
{state["question"]}

Order data:
{state["order_data"]}
"""
        )

        return {
            "answer": response.output_text
        }

    # -------------------------------------------------
    # NODE 4: ANSWER REFUND QUESTION
    # -------------------------------------------------

    async def answer_refund_question(state: SupportState):

        resource = await session.read_resource(
            "support://refund-policy"
        )

        refund_policy = get_text(resource.contents)

        prompt = await session.get_prompt(
            "evaluate_refund"
        )

        prompt_text = get_text(
            [
                message.content
                for message in prompt.messages
            ]
        )

        response = client.responses.create(
            model=MODEL,
            input=[
                {
                    "role": "system",
                    "content": prompt_text
                },
                {
                    "role": "user",
                    "content": f"""
Customer question:
{state["question"]}

Order data:
{state["order_data"]}

Refund policy:
{refund_policy}
"""
                }
            ]
        )

        return {
            "answer": response.output_text
        }

    # -------------------------------------------------
    # ROUTER
    # -------------------------------------------------

    def route_question(state: SupportState):
        return state["intent"]

    # -------------------------------------------------
    # BUILD GRAPH
    # -------------------------------------------------

    graph = StateGraph(SupportState)

    graph.add_node("classify", classify_intent)
    graph.add_node("get_order", get_order)
    graph.add_node(
        "answer_order",
        answer_order_question
    )
    graph.add_node(
        "answer_refund",
        answer_refund_question
    )

    graph.add_edge(START, "classify")
    graph.add_edge("classify", "get_order")

    graph.add_conditional_edges(
        "get_order",
        route_question,
        {
            "order_status": "answer_order",
            "refund": "answer_refund"
        }
    )

    graph.add_edge("answer_order", END)
    graph.add_edge("answer_refund", END)

    return graph.compile()


# =====================================================
# MAIN
# =====================================================

async def main():
    customer_id = int(
        input("Enter customer ID: ")
    )

    question = input(
        "Enter customer question: "
    )

    async with streamable_http_client(
        "http://localhost:8000/mcp"
    ) as (
        read_stream,
        write_stream,
        _
    ):
        async with ClientSession(
            read_stream,
            write_stream
        ) as session:

            await session.initialize()

            graph = create_graph(session)

            result = await graph.ainvoke({
                "customer_id": customer_id,
                "question": question,
                "intent": "",
                "order_data": "",
                "answer": ""
            })

            print(
                f"\nIntent: {result['intent']}"
            )

            print("\nAnswer:")
            print(result["answer"])


asyncio.run(main())