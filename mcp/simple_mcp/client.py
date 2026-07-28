from mcp import ClientSession
from mcp.client.streamable_http import streamable_http_client
import asyncio
from openai import OpenAI 
from dotenv import load_dotenv
import json 

# SETUP THE ENVIRONMENT
OPENAI_MODEL = "gpt-5.4-mini"
load_dotenv()
client = OpenAI()

# CONVERT TOOL DATA TO OPENAI SCHEMA
def convert_tool_to_openai_schema(tool):
    return {
        "type": "function",
        "name": tool.name,
        "description": tool.description,
        "parameters": tool.inputSchema
    }

# CONNECT TO THE MCP SERVER
async def main():
    query = input("Enter human query: ")
    async with streamable_http_client("http://localhost:8000/mcp") as (
        read_stream,
        write_stream,
        input_stream
    ):
        async with ClientSession(read_stream, write_stream) as session:
            # WAIT FOR SESSION TO INITIALIZE
            await session.initialize()
            # LIST AVAILABLE TOOLS ON THE MCP SERVER
            tool_list = await session.list_tools()
            openai_tools = []
            for t in tool_list.tools:
                openai_tools.append(convert_tool_to_openai_schema(t))
            response = client.responses.create(
                model=OPENAI_MODEL,
                input=query,
                tools=openai_tools
            )
            tool_call = None
            for item in response.output:
                if item.type == "function_call":
                    tool_call = item
                    break
            if tool_call:
                tool_name = tool_call.name
                args = json.loads(tool_call.arguments)
                print(f"LLM SELECTED TOOL: {tool_name}")
                result = await session.call_tool(tool_name,args)
                print(result)
            else:
                print("NO TOOL SELECTED. USING INTERNAL KNOWLEDGE.")
                print(response.output_text)

            


asyncio.run(main())