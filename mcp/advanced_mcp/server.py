from mcp.server.fastmcp import FastMCP
import requests
import wikipedia


mcp = FastMCP(
    "Customer Support MCP Server",
    json_response=True
)


# =====================================================
# TOOLS
# =====================================================

@mcp.tool()
def get_order_data(customer_id: int):
    """
    Get the customer's order information.

    Returns:
    - Item name
    - Delivery date
    - Delivery status
    - Number of delayed days
    """
    url = f"http://localhost:8080/delivery/{customer_id}"

    try:
        response = requests.get(url, timeout=10)

        if response.status_code != 200:
            return {
                "error": "Order data not found"
            }

        return {
            "data": response.json()
        }

    except requests.RequestException as error:
        return {
            "error": f"Could not contact order service: {error}"
        }


@mcp.tool()
def get_wiki_data(topic: str):
    """
    Get a Wikipedia summary for a topic.
    """
    try:
        return {
            "data": wikipedia.summary(
                topic,
                sentences=10
            )
        }

    except Exception as error:
        return {
            "error": str(error)
        }


# =====================================================
# RESOURCE
# =====================================================

@mcp.resource(
    "support://refund-policy",
    name="Refund Policy",
    description="Company policy for refunds, damaged products, and lost shipments",
    mime_type="text/plain" #multipurpose internet mail extensions \ media type
)
def refund_policy():
    """
    Return the official customer refund policy.
    """
    return """
CUSTOMER REFUND POLICY

1. Damaged products
Customers are eligible for a full refund when the product arrives damaged.
The customer must report the damage within 7 days of delivery.

2. Lost shipments
A shipment marked as lost in transit is eligible for a full refund after
the shipment has been delayed for at least 7 days.

3. Delayed shipments
A delayed shipment is not automatically eligible for a refund.
A refund may be approved if the shipment remains undelivered for more than
7 days after the expected delivery date.

4. Delivered products
Products may be returned within 30 days of delivery if they are unused and
in their original packaging.

5. Non-refundable charges
Express-delivery charges are non-refundable unless the shipment was lost.

6. Refund processing
Approved refunds are returned to the original payment method within
5 to 7 business days.
"""


# =====================================================
# PROMPT
# =====================================================

@mcp.prompt(
    name="evaluate_refund",
    description="Evaluate whether a customer qualifies for a refund"
)
def evaluate_refund():
    """
    Return standardized instructions for evaluating refund requests.
    """
    return """
You are a professional customer-support refund specialist.

Evaluate the customer's refund request using only:

1. The supplied customer order data.
2. The supplied official refund policy.
3. The customer's question.

Instructions:

- Determine whether the customer is eligible for a refund.
- Do not invent missing order information.
- Clearly state one decision:
  - Eligible
  - Not currently eligible
  - More information required
- Explain the reason for the decision.
- Mention the applicable refund-policy rule.
- Explain the next steps the customer should take.
- Do not claim that a refund has already been processed.
- Be polite, concise, and professional.
"""


# =====================================================
# START MCP SERVER
# =====================================================

if __name__ == "__main__":
    mcp.run(transport="streamable-http")