from huggingface_hub import InferenceClient

client = InferenceClient(
    "mistralai/Mistral-Nemo-Instruct-2407",
    token="hf_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
)

for message in client.chat_completion(
	messages=[{"role": "user", "content": "What is the capital of France?"}],
	max_tokens=500,
	stream=True,
):
    print(message.choices[0].delta.content, end="")