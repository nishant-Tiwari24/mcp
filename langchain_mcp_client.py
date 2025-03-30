import asyncio

from dotenv import load_dotenv
from langchain_core.messages import ToolMessage, AIMessage
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent

from langchain_openai import ChatOpenAI

load_dotenv()
model = ChatOpenAI(model="gpt-4o")


async def main():
    prompt = """Always use the arxiv_server tool to answer a question"""
    async with MultiServerMCPClient(
            {
                # "math": {
                #     "command": "python",
                #     # Make sure to update to the full absolute path to your math_server.py file
                #     "args": ["/path/to/math_server.py"],
                #     "transport": "stdio",
                # },
                "arxiv_server": {
                    # make sure you start your weather server on port 8000
                    "url": "http://127.0.0.1:8000/sse",
                    "transport": "sse",
                }
            }
    ) as client:
        print("rajib ", client.get_tools())
        agent = create_react_agent(model, client.get_tools(), prompt=prompt)
        # math_response = await agent.ainvoke({"messages": "what's (3 + 5) x 12?"})
        arxiv_response = await agent.ainvoke({"messages": "I want to know about Neural Network architecture?"})
        messages = arxiv_response["messages"]

        for message in messages:
            if isinstance(message, AIMessage):
                print(message.content)


asyncio.run(main())
