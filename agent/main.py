import asyncio
import os
from pydantic_ai import Agent
from dotenv import load_dotenv
import logfire
from .tools import get_server_stats, get_server_logs, restart_server

# Load env vars
load_dotenv()

# Configure logfire
# logfire.configure()

# Define the agent
agent = Agent(
    'google-gla:gemini-flash-latest',
    system_prompt=(
        "You are an SRE. Monitor 'production-server'. "
        "Check stats and logs. "
        "If memory > 50MB or logs contain 'WARNING', restart the container. "
        "Otherwise, report status."
    ),
)

# Register tools
agent.tool_plain(get_server_stats)
agent.tool_plain(get_server_logs)
agent.tool_plain(restart_server)

async def main():
    print("SRE Agent started. Monitoring 'production-server'...", flush=True)
    
    while True:
        try:
            # Run the agent
            result = await agent.run("Check system health for 'production-server'")
            print(f"Agent Action: {result}", flush=True)
        except Exception as e:
            print(f"Agent Error: {e}", flush=True)
        
        await asyncio.sleep(20)

if __name__ == "__main__":
    asyncio.run(main())
