import subprocess
import sys
import traceback

from langchain_core.tools import Tool
from langchain_experimental.utilities import PythonREPL

python_repl = PythonREPL()

def test_agent(requirements, code_template):
    logs = []
    logs.append("Starting package installation...")

    # Install packages
    for package in requirements.splitlines():
        if package.strip():
            try:
                subprocess.check_call([sys.executable, "-m", "pip", "install", package])
                logs.append(f"Successfully installed {package}")
            except subprocess.CalledProcessError as e:
                logs.append(f"Failed to install {package}. Error: {str(e)}")
                return False, logs

    logs.append("Starting code execution...")

    # Execute code
    try:
        code = python_repl.run(code_template)
        logs.append("Generated code output:")
        logs.append(code)
        logs.append("Code executed successfully.")
        return True, logs
    except Exception as e:
        logs.append("An error occurred during code execution:")
        logs.append(traceback.format_exc())
        return False, logs

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
