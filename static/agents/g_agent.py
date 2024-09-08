import os
import sys
from langchain_anthropic import ChatAnthropic
from langchain_core.messages import HumanMessage
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import create_react_agent
from dotenv import load_dotenv
from langchain_googledrive.tools.google_drive.tool import GoogleDriveSearchTool
from langchain_googledrive.utilities.google_drive import GoogleDriveAPIWrapper




# Load environment variables from the .env file
load_dotenv()

# Get the environment variables for the API keys
anthropic_api_key = os.getenv("ANTHROPIC_API_KEY")
serp_api_key = os.getenv("SERPAPI_API_KEY")


#tools
folder_id = "root"
# folder_id='1yucgL9WGgWZdM1TOuKkeghlPizuzMYb5'

# By default, search only in the filename.
tool = GoogleDriveSearchTool(
    name="google_drive_search",  # Set a valid name
    api_wrapper=GoogleDriveAPIWrapper(
        folder_id=folder_id,
        num_results=2,
        template="gdrive-query-in-folder",  # Search in the body of documents
    )
)


# Create the agent
memory = MemorySaver()
model = ChatAnthropic(model_name="claude-3-sonnet-20240229", api_key=anthropic_api_key)

# Combine tools
tools = [tool]

agent_executor = create_react_agent(model, tools, checkpointer=memory)

# Configuration for the agent
config = {"configurable": {"thread_id": "abc123"}}



# Use the agent in a loop
while True:
    prompt = input("Enter a prompt: ")

    # Use the agent to handle the user prompt
    for chunk in agent_executor.stream(
        {"messages": [HumanMessage(content=prompt)]}, config
    ):
        print(chunk)
        print("----")


