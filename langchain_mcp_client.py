import asyncio
from dotenv import load_dotenv
from langchain_core.messages import ToolMessage, AIMessage, HumanMessage
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent
from langchain_openai import ChatOpenAI
from langgraph.checkpoint.memory import MemorySaver
from typing import Dict, Any

# Multi-server configuration
SERVERS = {
    "jobs_server": {
        "url": "http://127.0.0.1:8000/sse",
        "transport": "sse",
    },
    "employee_server": {
        "url": "http://127.0.0.1:8002/sse", 
        "transport": "sse",
    }
}

# Enhanced prompt with more detailed instructions
def get_prompt_and_query():
    prompt = """You are a helpful AI assistant with access to two specialized servers:

1. **Jobs Server** (find_similar_jobs tool):
   - Use this tool to find similar job requisitions
   - Input: job requirements, skills, location, experience level
   - Output: list of matching job opportunities

2. **Employee Server** (summarize_employee_feedback tool):
   - Use this tool to get employee feedback summaries
   - Input: employee name (exact match required)
   - Output: feedback summary for the current year (2024)

**Instructions:**
- Choose the appropriate tool based on the user's question
- For job searches, provide detailed requirements
- For employee feedback, use the exact employee name as stored in the system
- If multiple tools are needed, execute them in sequence
- Provide clear, structured responses with relevant details
- If a tool fails, explain the issue and suggest alternatives

**Available employees:** Kalyan P., Alex J."""
    
    query = (
        "I need to find similar jobs for an AI engineer position in San Jose, CA with 4-5 years of experience, "
        "and also get a feedback summary for Kalyan P. Can you help me with both?"
    )
    return prompt, query

load_dotenv()

# Enhanced model configuration
model = ChatOpenAI(
    model="gpt-4o",
    temperature=0.1,  # Lower temperature for more consistent responses
    max_tokens=4000,  # Increased token limit for detailed responses
    request_timeout=60  # 60 second timeout
)

async def main():
    prompt, query = get_prompt_and_query()
    
    # Create multi-server client
    client = MultiServerMCPClient(SERVERS)
    
    # Get tools from all servers
    tools = await client.get_tools()
    print(f"Available tools: {[tool.name for tool in tools]}")
    
    # Create memory saver for conversation history
    memory = MemorySaver()
    
    # Create agent with enhanced parameters
    agent = create_react_agent(
        model, 
        tools, 
        prompt=prompt,
        debug=True  # Enable debug mode for better error handling
    )
    
    # Create initial state with the user query
    initial_state = {
        "messages": [HumanMessage(content=query)],
        "chat_history": []
    }
    
    # Run the agent with enhanced configuration
    try:
        response = await agent.ainvoke(initial_state)
        messages = response["messages"]
        
        print("\n=== Agent Response ===")
        for message in messages:
            if isinstance(message, AIMessage):
                print(message.content)
        
        # Print additional debug information
        print(f"\n=== Debug Info ===")
        print(f"Total messages: {len(messages)}")
        print(f"Final state keys: {list(response.keys())}")
        
    except Exception as e:
        print(f"Error during agent execution: {e}")
        print("This might be due to tool execution issues or server connectivity problems.")

if __name__ == "__main__":
    asyncio.run(main())
