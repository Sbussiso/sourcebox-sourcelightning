import os
import sys
from langchain_anthropic import ChatAnthropic
from langchain_core.messages import HumanMessage
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import create_react_agent
from dotenv import load_dotenv
from tempfile import TemporaryDirectory

from langchain_googledrive.tools.google_drive.tool import GoogleDriveSearchTool
from langchain_googledrive.utilities.google_drive import GoogleDriveAPIWrapper
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# Load environment variables from the .env file
load_dotenv()

# Check if GOOGLE_ACCOUNT_FILE is set correctly
gdrive_file = os.getenv("GOOGLE_ACCOUNT_FILE")
print(f"Google credentials file: {gdrive_file}")

# Check if the file exists
if not os.path.exists(gdrive_file):
    raise FileNotFoundError(f"Google credentials file not found: {gdrive_file}")

# OAuth 2.0 Authorization Flow with Manual Code Entry (No Web Server)
SCOPES = ['https://www.googleapis.com/auth/drive']
token_path = "token.json"

# Load existing credentials if available
creds = None
if os.path.exists(token_path):
    creds = Credentials.from_authorized_user_file(token_path, SCOPES)

# If no valid credentials, start the OAuth flow
if not creds or not creds.valid:
    flow = InstalledAppFlow.from_client_secrets_file(gdrive_file, SCOPES)
    auth_url, _ = flow.authorization_url(prompt='consent')

    # Print the authorization URL for the user to visit
    print(f"Please go to this URL and authorize access: {auth_url}")

    # Ask the user to paste the authorization code
    auth_code = input("Enter the authorization code: ")

    # Fetch the credentials using the authorization code
    creds = flow.fetch_token(code=auth_code)

    # Save the credentials for future use
    with open(token_path, 'w') as token:
        token.write(creds.to_json())

# Initialize Google Drive API service
service = build('drive', 'v3', credentials=creds)

# Initialize Google Drive search tool
folder_id = "root"  # You can set this to any folder ID you want to search in Google Drive
tool = GoogleDriveSearchTool(
    api_wrapper=GoogleDriveAPIWrapper(
        folder_id=folder_id,
        num_results=2,
        template="gdrive-query-in-folder",  # Search in the body of documents
    )
)

# Example search query
result = tool.run("machine learning")
print(result)

# Get the environment variables for the API keys
anthropic_api_key = os.getenv("ANTHROPIC_API_KEY")

# Initialize LangChain agent components
memory = MemorySaver()
model = ChatAnthropic(model_name="claude-3-sonnet-20240229", api_key=anthropic_api_key)

# Placeholder for when agent integration is needed
agent_executor = create_react_agent(model, [tool], checkpointer=memory)

# Configuration for the agent
config = {"configurable": {"thread_id": "abc123"}}

# Exit the script
sys.exit()


# Create the agent
memory = MemorySaver()
model = ChatAnthropic(model_name="claude-3-sonnet-20240229", api_key=anthropic_api_key)

# Combine tools
tools = []

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
