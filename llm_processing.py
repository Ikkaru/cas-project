import os
import asyncio
import json
from pathlib import Path
from groq import AsyncGroq
from dotenv import load_dotenv

HISTORY_FILE = 'chat_history.json'
PERSONA_FILE = "persona.txt"

# Create Groq client
dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path)
client = AsyncGroq(
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

PERSONA = load_system_prompt(PERSONA_FILE)

# Load History
async def load_history():
    history_path = Path(HISTORY_FILE)
    if history_path.exists():
        try:
            with open (history_path, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            print("Warning: Json File is Empty")
            return [{"role": "system", "content": PERSONA}]
        else:
            print("Eror: Cannot load chat history file")
            exit(1)

# Save chat histroy
async def save_history(message):
    with open(HISTORY_FILE, 'w') as f:
        json.dump(message, f, indent=2)
        
# Response Processing
async def llm_response(input) -> None:
    # Set system prompt (Load the persona)
    system_prompt = {
        "role" : "system",
        "content": PERSONA
    }

    try:    
        # Initialize chat history
        chat_history = await load_history()

        # Append the user input to the history
        chat_history.append({"role": "user", "content": input})

        stream = await client.chat.completions.create(
            messages = chat_history,
            temperature = 1,
            model= "llama-3.1-8b-instant",
            stream=True,
        )

        response = ""
        async for chunk in stream:
            content = chunk.choices[0].delta.content
            if content:
                response += content
                print(content, end="")
            if chunk.choices[0].finish_reason:
                if chunk.x_groq is None and chunk.x_groq.usage is None:
                    print(f"\n Ussage stats: {chunk.x_groq.usage}")

        # Append the response to chat history
        chat_history.append({
            "role" : "assistant",
            "content" : response
        })
        await save_history(chat_history)
        print("\n")

    # cancel on keyboard interrupt
    except KeyboardInterrupt:
        print("Session Terminated")
    finally:
        await save_history(chat_history)