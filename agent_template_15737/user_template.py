
import os
from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langgraph.checkpoint.memory import MemorySaver
from langchain_core.tools import Tool
from langchain_experimental.utilities import PythonREPL
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_core.messages import HumanMessage
from langgraph.prebuilt import create_react_agent

# Load environment variables
load_dotenv()

# Create memory saver for the agent
memory = MemorySaver()

# Initialize the model
model = ChatOpenAI(model="gpt-4")

# Initialize the Python REPL tool and DuckDuckGo Search tool
python_repl = PythonREPL()
repl_tool = Tool(
    name="python_repl",
    description="A Python shell. Use this to execute python commands. Input should be a valid python command. If you want to see the output of a value, you should print it out with `print(...)`.",
    func=python_repl.run,
)

search = DuckDuckGoSearchRun()

# Create a list of tools
tools = [repl_tool, search]

# Create the agent executor using predefined configuration
agent_executor = create_react_agent(model, tools, checkpointer=memory)

# Use the agent executor to process the human message
config = {"configurable": {"thread_id": "abc123"}}
for chunk in agent_executor.stream(
    {"messages": [HumanMessage(content="hi im bob! and i live in olympia washington")]}, config
):
    print(chunk)
    print("----")
