from dotenv import load_dotenv
import os
from groq import Groq

# Load environment variables from the .env file
load_dotenv()

# Fetch the API key
api_key = os.getenv("GROQ_API_KEY")

# Initialize the Groq client with the API key
client = Groq(api_key=api_key)

# Define the chat completion request
chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "system",
            "content": "you are a helpful assistant."
        },
        {
            "role": "user",
            "content": "Write short script for kids to learn about the islamic stories",
        }
    ],
    model="llama3-8b-8192",
    temperature=0.5,
    max_tokens=1024,
    top_p=1,
    stop=None,
    stream=False,
)

# Print the response
print(chat_completion.choices[0].message.content)
