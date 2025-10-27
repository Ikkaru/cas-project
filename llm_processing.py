import os
from groq import Groq
from dotenv import load_dotenv

# Create Groq client

client = Groq(
    api_key=os.environ.get("API_KEY")
)

# Load the persona file 
def load_system_prompt(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        print(f"Error: File prompt tidak ditemukan di {file_path}")
        return None

PERSONA_FILE = "persona.txt"
PERSONA = load_system_prompt(PERSONA_FILE)

# Set system prompt (Load the persona)
system_prompt = {
    "role" : "system",
    "content": PERSONA
}

# Initialize chat history
chat_history = [system_prompt]

# Get user input from the console
user_input = input("You: ")

# Append the user input to the history
chat_history.append({"role": "user", "content": user_input})

response = client.chat.completions.create(
    messages = chat_history,
    max_tokens = 100,
    temperature = 1,
    model= "llama-3.1-8b-instant"
)

# Append the response to chat history
chat_history.append({
    "role" : "assistant",
    "content" : response.choices[0].message.content
})

print(response.choices[0].message.content)