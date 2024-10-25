```python
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langgraph.checkpoint.memory import MemorySaver
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage
from langgraph.prebuilt import create_react_agent

load_dotenv()

# Initialize memory saver and model
memory = MemorySaver()
model = ChatOpenAI(model="gpt-4")

# Define tools
search = DuckDuckGoSearchRun()

@tool
def multiply(a: int, b: int) -> int:
    """Multiply two numbers."""
    return a * b

# Combine tools
tools = [search, multiply]

# Create agent with specified tools
agent_executor = create_react_agent(model, tools, checkpointer=memory)

# Use the agent
config = {"configurable": {"thread_id": "abc123"}}
for chunk in agent_executor.stream(
    {"messages": [HumanMessage(content="hi im bob! and i live in olympia washington")]}, config
):
    print(chunk)
    print("----")
    
# Inspect multiply tool attributes
print(multiply.name)
print(multiply.description)
print(multiply.args)
```
