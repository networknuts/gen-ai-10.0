from mcp.server.fastmcp import FastMCP
import requests
import wikipedia

mcp = FastMCP("Customer Support MCP Server", json_response=True)

@mcp.tool()
def get_order_data(customer_id: int):
    """
    Get the following information about the ordered item of a customer:
    - Item name
    - Delivery date
    - Delivery status

    This function requires a customer_id to get the data of the order
    of the particular customer.
    """
    url = f"http://localhost:8080/delivery/{customer_id}"
    response = requests.get(url)
    if response.status_code != 200:
        return {
            "Error": "Order data not found"
        }
    else:
        return {
            "Data": response.json()
        }

@mcp.tool()
def get_wiki_data(topic: str):
    """
    Get wikipedia summary of any topic by providing the topic's name.
    This wikipedia function will only provide a 10 line summary of
    the given topic.
    """
    try:
        return {
            "Data": wikipedia.summary(topic,sentences=10)
        }
    except Exception as e:
        return {
            "Error": str(e)
        }

mcp.run(transport="streamable-http")