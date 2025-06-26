import asyncio
from dotenv import load_dotenv
from langchain_core.messages import ToolMessage, AIMessage
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent
from langchain_openai import ChatOpenAI

# === Choose which server to use: "jobs_server" or "employee_server" ===
SERVER = "jobs_server"  # or "employee_server"

# Example queries for each server
def get_prompt_and_query(server):
    if server == "jobs_server":
        prompt = """Always use the find_similar_jobs tool to answer a question about job requisitions."""
        query = (
            "I am looking for an AI engineer in San Jose, CA with 4-5 years of experience leveraging models like GPT 401, Claude 3.5 or similar. Can you please show the similar jobs I can use to create a requisition?"
        )
    else:
        prompt = """Always use the summarize_employee_feedback tool to answer a question about employee feedback summaries."""
        query = (
            "I am requesting a feedback summary for Kalyan P. The system will pull calendar year feedback, including Props, and create a summary for me to review, which can be ideally entered into Workday as an impact summary."
        )
    return prompt, query

load_dotenv()
model = ChatOpenAI(model="gpt-4o")

async def main():
    prompt, query = get_prompt_and_query(SERVER)
    client = MultiServerMCPClient(
        {
            SERVER: {
                "url": "http://127.0.0.1:8000/sse",
                "transport": "sse",
            }
        }
    )
    tools = await client.get_tools()
    agent = create_react_agent(model, tools, prompt=prompt)
    response = await agent.ainvoke({"messages": query})
    messages = response["messages"]
    for message in messages:
        if isinstance(message, AIMessage):
            print(message.content)

# now lets execute
asyncio.run(main())
