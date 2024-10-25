```python
from dotenv import load_dotenv
import os
from langchain_openai import ChatOpenAI
from langgraph.checkpoint.memory import MemorySaver
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage
from langgraph.prebuilt import create_react_agent

# Load environment variables
load_dotenv()

# Create the model and memory saver
model = ChatOpenAI(model="gpt-4")
memory = MemorySaver()

# Define tools
@tool
def multiply(a: int, b: int) -> int:
    """Multiply two numbers."""
    return a * b

# Let's inspect some of the attributes associated with the tool.
print(multiply.name)
print(multiply.description)
print(multiply.args)

# Assign tools
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
```