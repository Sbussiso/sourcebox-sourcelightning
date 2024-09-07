import os
import sys
import platform
from langchain_anthropic import ChatAnthropic
from langchain_core.messages import HumanMessage
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import create_react_agent
from dotenv import load_dotenv
from langchain_community.tools import ShellTool
from tempfile import TemporaryDirectory
from langchain_community.agent_toolkits import FileManagementToolkit

# Check for admin/root privileges based on the OS
is_windows = platform.system() == "Windows"

if is_windows:
    import ctypes
    
    def is_admin():
        """Check if the script is running with admin privileges on Windows."""
        try:
            return ctypes.windll.shell32.IsUserAnAdmin()
        except:
            return False

    if not is_admin():
        print("Requesting admin privileges...")
        # Re-run the script with admin privileges
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
        sys.exit()

else:
    def is_root():
        """Check if the script is running as root on Linux/macOS."""
        return os.geteuid() == 0

    if not is_root():
        print("This script requires elevated permissions. Please run with sudo.")
        sys.exit()

# Load environment variables from the .env file
load_dotenv()

# Get the environment variables for the API keys
anthropic_api_key = os.getenv("ANTHROPIC_API_KEY")

# We'll make a temporary directory to avoid clutter
working_directory = TemporaryDirectory()

# Create a File Management Toolkit
toolkit = FileManagementToolkit(
    root_dir=str(working_directory.name)
)  # If you don't provide a root_dir, operations will default to the current working directory

# Get the tools from the toolkit
file_management_tools = toolkit.get_tools()

# Initialize other tools
shell_tool = ShellTool()

# Create the agent
memory = MemorySaver()
model = ChatAnthropic(model_name="claude-3-sonnet-20240229", api_key=anthropic_api_key)

# Combine tools (shell tool + file management tools)
tools = [shell_tool] + file_management_tools  # Add all tools to the agent

agent_executor = create_react_agent(model, tools, checkpointer=memory)

# Configuration for the agent
config = {"configurable": {"thread_id": "abc123"}}

# Get the OS name
os_name = platform.system()

# Use the agent in a loop
while True:
    prompt = input("Enter a prompt: ")

    # Use the agent to handle the user prompt
    for chunk in agent_executor.stream(
        {"messages": [HumanMessage(content=prompt)]}, config
    ):
        print(chunk)
        print("----")
