from openai import OpenAI, OpenAIError, RateLimitError, APIError, Timeout
import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Ensure the API key is loaded
try:
    client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
except Exception as e:
    print(f"Error initializing OpenAI client: {e}")
    exit(1)

# List to store conversation history
conversation_history = []

def gpt_response(user_input):
    print("Generating response...\n")
    """
    Generate a response from GPT-4 based on user input and conversation history.
    """
    try:
        # Send the entire conversation history to GPT-4
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": """You are a helpful assistant.
                                                    PROMPT = the users prompt
                                                    HISTORY = the conversation history"""},
                                                    
                {"role": "user", "content": f"PROMPT: {user_input} HISTORY: {conversation_history}"}
            ]
        )

        # Extract the assistant's reply
        assistant_reply = response.choices[0].message.content

        # Add the assistant's reply to the conversation history
        conversation_history.append({"role": "assistant", "content": assistant_reply})

        return assistant_reply

    except RateLimitError:
        return "Error: Rate limit exceeded. Try again later."
    except Timeout:
        return "Error: Request timed out. Try again."
    except APIError as e:
        return f"Error: OpenAI API error: {e}"
    except OpenAIError as e:
        return f"Error: Unable to communicate with OpenAI API: {e}"

def run_chatbot():
    print("\nWelcome to the GPT-4 Command Line Chatbot!\n")
    print("Type 'exit' to end the conversation.\n")

    while True:
        user_input = input("You: ")

        if user_input.lower() == 'exit':
            print("Goodbye!")
            break

        response = gpt_response(user_input)
        print(f"GPT-4: {response}\n")

if __name__ == "__main__":
    run_chatbot()
