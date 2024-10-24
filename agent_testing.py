import subprocess
import sys
import traceback

from langchain_core.tools import Tool
from langchain_experimental.utilities import PythonREPL

python_repl = PythonREPL()

def test_agent(requirements, code_template):
    """Install packages using pip."""
    # Remove standard library modules from the requirements list
    standard_libs = {'os'}
    requirements_list = [
        req.strip() for req in requirements.splitlines() 
        if req.strip() and req.strip() != '```' and req.strip() not in standard_libs
    ]
    print("Requirements to install:", requirements_list)  # Log the requirements list

    for package in requirements_list:
        print(f"Attempting to install package: {package}")  # Debugging log
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
            print(f"Successfully installed {package}")
        except subprocess.CalledProcessError as e:
            print(f"Failed to install {package}. Error: {str(e)}")
            return False  # Return False if any package installation fails

    """Run the generated code and check for errors."""
    print("Starting code execution...")  # Debugging log
    try:
        # Use exec to run the generated code
        code = python_repl.run(code_template)
        print("Generated code output:")  # Debugging log
        print(code)
        print("Code executed successfully.")
        return True  # Return True if code execution is successful

    except Exception as e:
        # Capture and print any errors that occur during execution
        print("An error occurred during code execution:")
        traceback.print_exc()
        return False  # Return False if code execution fails

if __name__ == "__main__":
    print("Starting agent test...")  # Debugging log
    required_packages = [
    'langchain_anthropic', 'langchain_core', 'langgraph',
    'langchain_community', 'python-dotenv', 'anthropic',
    'duckduckgo-search', 'wikipedia'
    ]

    code_template = """
import os
from dotenv import load_dotenv

from langchain_anthropic import ChatAnthropic
from langchain_core.messages import HumanMessage
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import create_react_agent

from langchain_community.tools import DuckDuckGoSearchRun, WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper

# Load environment variables
load_dotenv()

# Initialize memory saver
memory = MemorySaver()

# Initialize models and tools
model = ChatAnthropic(model="claude-3-sonnet-20240229")
search_tool = DuckDuckGoSearchRun()
wikipedia_api = WikipediaAPIWrapper()
wiki_tool = WikipediaQueryRun(api_wrapper=wikipedia_api)

# Compile list of tools
tools = [search_tool, wiki_tool]

# Create the agent
agent_executor = create_react_agent(model, tools, checkpointer=memory)

# Define configuration
config = {"configurable": {"thread_id": "abc123"}}

# Use the agent
for chunk in agent_executor.stream(
    {"messages": [HumanMessage(content="hi im bob! and i live in olympia washington")]}, config
):
    print(chunk)
    print("----")
"""

    test = test_agent(required_packages, code_template)
    print(f"Test result: {test}")  # Debugging log
