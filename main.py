import llm_processing
import asyncio


if __name__ == "__main__":
    try:
        while True:
            user_input = input("Input: ")
            if user_input.lower() in ['exit', 'quit', 'q']:
                break
            asyncio.run(llm_processing.llm_response(user_input))
    except KeyboardInterrupt:
        print("\nSession Terminated (Keyboard Interupt)")
        exit(0)