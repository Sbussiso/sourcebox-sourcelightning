
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

from langchain_mistralai import ChatMistralAI
from langgraph.checkpoint.memory import MemorySaver
import nest_asyncio
from langchain_community.utilities.wolfram_alpha import WolframAlphaAPIWrapper
from langchain_core.tools import Tool
from langchain_experimental.utilities import PythonREPL
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.messages import HumanMessage
from langgraph.prebuilt import create_react_agent

# Nest asyncio to avoid event loop issues
nest_asyncio.apply()

# Create memory saver
memory = MemorySaver()

# Initialize ChatMistralAI model
model = ChatMistralAI(model="mistral-large-latest")

# Initialize WolframAlpha tool
wolfram = WolframAlphaAPIWrapper()

# Initialize PythonREPL tool
python_repl = PythonREPL()
repl_tool = Tool(
    name="python_repl",
    description="A Python shell. Use this to execute python commands. Input should be a valid python command. If you want to see the output of a value, you should print it out with `print(...)`.",
    func=python_repl.run,
)

# Initialize TavilySearchResults tool
search = TavilySearchResults(max_results=2)

# Compile all tools
tools = [wolfram, repl_tool, search]

# Create the agent using the model and tools
agent_executor = create_react_agent(model, tools, checkpointer=memory)

# Use the agent
config = {"configurable": {"thread_id": "abc123"}}
for chunk in agent_executor.stream(
    {"messages": [HumanMessage(content="hi im bob! and i live in olympia washington")]}, config
):
    print(chunk)
    print("----")

