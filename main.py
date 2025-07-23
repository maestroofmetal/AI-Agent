import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()   
api_key = os.environ.get("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)

def main():
    # Takes prompts from command line and exits if it's not found
    # e.g. --> uv run main.py "Prompt goes here"
    if len(sys.argv) < 2:
        print("No prompt entered!")
        sys.exit(1)
    prompt = sys.argv[1]
    
    # Stores conversation history
    messages = [
    types.Content(role="user", parts=[types.Part(text=prompt)]),
    ]
    
    response = client.models.generate_content(
    model='gemini-2.0-flash-001', contents=messages)
    print(response.text)
    
    # Used for debugging:
    # Collects token information from the usage metadata

    if len(sys.argv) > 2:
        if sys.argv[2] == "--verbose":
            prompt_tokens = response.usage_metadata.prompt_token_count
            response_tokens = response.usage_metadata.candidates_token_count
            
            print(f"User prompt: {prompt}")
            print(f"Prompt tokens: {prompt_tokens}")
            print(f"Response tokens: {response_tokens}")


if __name__ == "__main__":
    main()
