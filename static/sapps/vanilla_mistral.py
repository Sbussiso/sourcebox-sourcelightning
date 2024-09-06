from huggingface_hub import InferenceClient
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Initialize the HuggingFace Inference Client with the API key from .env
client = InferenceClient(
    model="mistralai/Mistral-Nemo-Instruct-2407",
    token=os.getenv("HUGGINGFACEHUB_API_TOKEN")
)

# List to store conversation history
conversation_history = []

def huggingface_response(user_input):
    print("Generating response...\n")
    """
    Generate a response from the HuggingFace model based on user input and conversation history.
    """
    try:
        # Add the user's input to the conversation history
        conversation_history.append({"role": "user", "content": user_input})

        # Concatenate the entire conversation history into a single prompt
        conversation_string = ""
        for message in conversation_history:
            conversation_string += f"{message['role']}: {message['content']}\n"

        # Send the concatenated conversation to the HuggingFace model
        response = client.chat_completion(
            messages=[{"role": "user", "content": conversation_string}],
            max_tokens=500,
            stream=False  # Change to True if you want streaming responses
        )

        # Extract the assistant's reply
        assistant_reply = response.choices[0].message.content

        # Add the assistant's reply to the conversation history
        conversation_history.append({"role": "assistant", "content": assistant_reply})

        return assistant_reply

    except Exception as e:
        return f"Error: Unable to communicate with HuggingFace API: {e}"

def run_chatbot():
    print("\nWelcome to the HuggingFace Command Line Chatbot!\n")
    print("Type 'exit' to end the conversation.\n")

    while True:
        user_input = input("You: ")

        if user_input.lower() == 'exit':
            print("Goodbye!")
            break

        # Generate a response and print it
        response = huggingface_response(user_input)
        print(f"HuggingFace: {response}\n")

if __name__ == "__main__":
    run_chatbot()
