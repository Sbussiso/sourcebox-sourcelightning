```python
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import create_react_agent

# Load environment variables
load_dotenv()

# Initialize Memory and Model
memory = MemorySaver()
model = ChatOpenAI(model="gpt-4")

# Define and register the tool
@tool
def multiply(a: int, b: int) -> int:
    """Multiply two numbers."""
    return a * b

# Create a list of tools 
search = DuckDuckGoSearchRun()
tools = [search, multiply]

# Create the agent
agent_executor = create_react_agent(model, tools, checkpointer=memory)

# Use the agent
config = {"configurable": {"thread_id": "abc123"}}
for chunk in agent_executor.stream(
    {"messages": [HumanMessage(content="hi im bob! and i live in olympia washington")]}, config
):
    print(chunk)
    print("----")
```