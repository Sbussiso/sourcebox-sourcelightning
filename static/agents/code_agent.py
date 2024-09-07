import os
import platform
from langchain_anthropic import ChatAnthropic
from langchain_core.messages import HumanMessage
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import create_react_agent
from dotenv import load_dotenv
from langchain_community.utilities import StackExchangeAPIWrapper
from langchain_experimental.utilities import PythonREPL
from langchain_core.tools import Tool

# Load environment variables from the .env file
load_dotenv()

# Get the environment variables for the API keys
anthropic_api_key = os.getenv("ANTHROPIC_API_KEY")

# Initialize Python REPL tool
python_repl = PythonREPL()

# Create a Tool instance from the PythonREPL tool
python_repl_tool = Tool.from_function(
    func=python_repl.run,
    name="PythonREPL",
    description="A tool to execute Python code within a REPL environment."
)

# Initialize StackExchange API Wrapper
stackexchange = StackExchangeAPIWrapper()

# Define a function to retrieve a StackExchange question (assuming this is the correct way)
def get_stackexchange_question(query: str):
    return stackexchange.run(query)

# Create a Tool instance for StackExchange API
stackexchange_tool = Tool.from_function(
    func=get_stackexchange_question,
    name="StackExchangeAPI",
    description="A tool to get related questions from StackExchange for code-related errors."
)

# Create the agent
memory = MemorySaver()
model = ChatAnthropic(model_name="claude-3-sonnet-20240229", api_key=anthropic_api_key)

# Combine tools
tools = [python_repl_tool, stackexchange_tool]

# Create the agent executor with tools and memory
agent_executor = create_react_agent(model, tools, checkpointer=memory)

# Configuration for the agent
config = {"configurable": {"thread_id": "abc123"}}

# Get the OS name
os_name = platform.system()

# Use the agent in a loop
while True:
    prompt = input("Enter a prompt (type 'exit' to quit): ")

    if prompt.lower() == "exit":
        print("Exiting the agent loop.")
        break

    # Use the agent to handle the user prompt
    for chunk in agent_executor.stream(
        {"messages": [HumanMessage(content=prompt)]}, config
    ):
        # If tool usage is requested, make sure the correct input is passed
        if hasattr(chunk, 'tools'):
            # Handle tool usage here
            tool_message = chunk.tools.messages[0]  # Access the tool message
            tool_name = tool_message.name
            code_snippet = tool_message.content
            
            if tool_name == "PythonREPL":
                # Execute the code in the Python REPL
                result = python_repl.run(code_snippet)
                print(result)
        else:
            print(chunk)
        print("----")
