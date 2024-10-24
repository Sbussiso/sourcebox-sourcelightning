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

# Initialize memory and model
memory = MemorySaver()
model = ChatNVIDIA(model="meta/llama3-70b-instruct")

# Define and assign tools
@tool
def multiply(a: int, b: int) -> int:
    """Multiply two numbers."""
    return a * b

# Print tool attributes
print(multiply.name)
print(multiply.description)
print(multiply.args)

# Add tools to the list
search = DuckDuckGoSearchRun()
tools = [search, multiply]

# Create the agent executor
agent_executor = create_react_agent(model, tools, checkpointer=memory)

# Use the agent
config = {"configurable": {"thread_id": "abc123"}}
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