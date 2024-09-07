import os
import sys
import platform
from langchain_anthropic import ChatAnthropic
from langchain_core.messages import HumanMessage
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import create_react_agent
from dotenv import load_dotenv
from langchain_community.agent_toolkits.github.toolkit import GitHubToolkit
from langchain_community.utilities.github import GitHubAPIWrapper



# Load environment variables from the .env file
load_dotenv()

# Get the environment variables for the API keys
anthropic_api_key = os.getenv("ANTHROPIC_API_KEY")
github_app_id = os.getenv("GITHUB_APP_ID")

# Check if API keys are loaded correctly
if not anthropic_api_key:
    print("Error: Missing ANTHROPIC_API_KEY in the environment variables.")
    sys.exit(1)

if not github_app_id:
    print("Error: Missing GITHUB_APP_ID in the environment variables.")
    sys.exit(1)



# Tools

# Initialize the GitHub API Wrapper with the GitHub App ID
github = GitHubAPIWrapper(github_app_id=github_app_id)
toolkit = GitHubToolkit.from_github_api_wrapper(github)
github_tools = toolkit.get_tools()

# Create the agent
memory = MemorySaver()
model = ChatAnthropic(model_name="claude-3-sonnet-20240229", api_key=anthropic_api_key)

# Combine tools
tools = [github_tools]  # Flattened list of tools from the toolkit

agent_executor = create_react_agent(model, tools, checkpointer=memory)

# Configuration for the agent
config = {"configurable": {"thread_id": "abc123"}}

# Get the OS name
os_name = platform.system()
print(f"Running on {os_name}")

# Use the agent in a loop
while True:
    try:
        prompt = input("Enter a prompt (type 'exit' to quit): ")
        
        if prompt.lower() == "exit":
            print("Exiting the agent loop.")
            break

        # Use the agent to handle the user prompt
        for chunk in agent_executor.stream(
            {"messages": [HumanMessage(content=prompt)]}, config
        ):
            print(chunk)
            print("----")
    except KeyboardInterrupt:
        print("\nExiting...")
        break
