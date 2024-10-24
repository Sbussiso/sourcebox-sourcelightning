```python
import os
from dotenv import load_dotenv

from langchain_nvidia_ai_endpoints import ChatNVIDIA
from langgraph.checkpoint.memory import MemorySaver

from langchain_community.tools import DuckDuckGoSearchRun
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage
from langgraph.prebuilt import create_react_agent

# Load environment variables
load_dotenv()

# Create the agent's memory saver
memory = MemorySaver()

# Initialize the model
model = ChatNVIDIA(model="meta/llama3-70b-instruct")

# Define tools
search = DuckDuckGoSearchRun()

@tool
def multiply(a: int, b: int) -> int:
    """Multiply two numbers."""
    return a * b

# Collect tools in a list
tools = [search, multiply]

# Inspect attributes of the multiply tool
print(multiply.name)
print(multiply.description)
print(multiply.args)

# Set up the agent executor with model, tools, and memory
agent_executor = create_react_agent(model, tools, checkpointer=memory)

# Use the agent
config = {"configurable": {"thread_id": "abc123"}}

# Process initial message
for chunk in agent_executor.stream(
    {"messages": [HumanMessage(content="hi im bob! and i live in olympia washington")]}, config
):
    print(chunk)
    print("----")

# Process additional user prompt
prompt = input("Enter a prompt: ")
for chunk in agent_executor.stream(
    {"messages": [HumanMessage(content=prompt)]}, config
):
    print(chunk)
    print("----")
```