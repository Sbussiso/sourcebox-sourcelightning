```python
from dotenv import load_dotenv
import os
from langchain_nvidia_ai_endpoints import ChatNVIDIA
from langgraph.checkpoint.memory import MemorySaver
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage
from langgraph.prebuilt import create_react_agent

# Load environment variables
load_dotenv()

# Create the agent
memory = MemorySaver()
model = ChatNVIDIA(model="meta/llama3-70b-instruct")

# Define tools
@tool
def multiply(a: int, b: int) -> int:
    """Multiply two numbers."""
    return a * b

search = DuckDuckGoSearchRun()
tools = [search, multiply]

# Inspect some of the attributes associated with the tool
print(multiply.name)
print(multiply.description)
print(multiply.args)

# Create agent executor
agent_executor = create_react_agent(model, tools, checkpointer=memory)

# Configuration for agent
config = {"configurable": {"thread_id": "abc123"}}

# Use the agent
for chunk in agent_executor.stream(
    {"messages": [HumanMessage(content="hi im bob! and i live in olympia washington")]}, config
):
    print(chunk)
    print("----")

prompt = input("Enter a prompt: ")
for chunk in agent_executor.stream(
    {"messages": [HumanMessage(content=prompt)]}, config
):
    print(chunk)
    print("----")
```