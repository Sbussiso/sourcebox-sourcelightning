import anthropic
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Initialize the Anthropics client
client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

# List to store conversation history
conversation_history = []

def claude_response(user_input):
    print("Generating response...\n")
    """
    Generate a response from Claude based on user input and conversation history.
    """
    try:
        # Create the conversation prompt including user input and conversation history
        conversation = f"PROMPT: {user_input} HISTORY: {conversation_history}"

        # Send the entire conversation to Claude using the Messages API
        response = client.completions.create(
            model="claude-2",  # Use Claude-2 as the model (replace with the correct supported model)
            max_tokens_to_sample=1000,  # Set max tokens for response
            temperature=0,  # Set temperature for deterministic or more creative responses
            prompt=f"""{anthropic.HUMAN_PROMPT} {conversation} {anthropic.AI_PROMPT}"""
        )

        # Extract the assistant's reply by accessing the `completion` attribute directly
        assistant_reply = response.completion

        # Add the assistant's reply to the conversation history
        conversation_history.append({"role": "assistant", "content": assistant_reply})

        return assistant_reply

    except Exception as e:
        return f"Error: Unable to communicate with Claude API: {e}"

def run_chatbot():
    print("\nWelcome to the Claude Command Line Chatbot!\n")
    print("Type 'exit' to end the conversation.\n")

    while True:
        user_input = input("You: ")

        if user_input.lower() == 'exit':
            print("Goodbye!")
            break

        # Append user input to the conversation history
        conversation_history.append({"role": "user", "content": user_input})

        response = claude_response(user_input)
        print(f"Claude: {response}\n")

if __name__ == "__main__":
    run_chatbot()
