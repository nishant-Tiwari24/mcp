import asyncio

from dotenv import load_dotenv
from langchain_core.messages import ToolMessage, AIMessage
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent

from langchain_openai import ChatOpenAI

load_dotenv()
model = ChatOpenAI(model="gpt-4o")


async def main():
    # Ensuring the REACT AGENT always calls a tool
    prompt = """Always use the arxiv_server tool to answer a question"""

    # This is the Langchain MCP adapater for MCP servers
    async with MultiServerMCPClient(
            {
                "arxiv_server": {
                    # you need run the server.py to have the mcp server run on 8000
                    "url": "http://127.0.0.1:8000/sse",
                    "transport": "sse",
                }
            }
    ) as client:
        agent = create_react_agent(model, client.get_tools(), prompt=prompt)
        arxiv_response = await agent.ainvoke({"messages": "I want to know about Neural Network architecture?"})
        messages = arxiv_response["messages"]

        for message in messages:
            if isinstance(message, AIMessage):
                print(message.content)


# now lets execute
asyncio.run(main())
