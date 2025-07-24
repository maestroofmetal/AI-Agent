import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from config import system_prompt
from functions.get_file_content import *
from functions.get_files_info import *
from functions.write_file import *
from functions.run_python_file import *
from functions.call_function import *


load_dotenv()   
api_key = os.environ.get("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)

# Lists the functions available
available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_run_python_file,
        schema_write_file,
    ]
)

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
    
    # Used for debugging: Collects token information from the usage metadata
    verbose_arg = False
    if len(sys.argv) > 2:
        if sys.argv[2] == "--verbose":
            verbose_arg = True
    
    response = client.models.generate_content(
    model='gemini-2.0-flash-001',
    contents=messages,
    config=types.GenerateContentConfig(
        tools=[available_functions],
        system_instruction=system_prompt),
    )
    
    # Generates token information
    if verbose_arg:
        prompt_tokens = response.usage_metadata.prompt_token_count
        response_tokens= response.usage_metadata.candidates_token_count
        print(f"User prompt: {prompt}")
        print(f"Prompt tokens: {prompt_tokens}")
        print(f"Response tokens: {response_tokens}")
    
    # Handles function calls if present and explains what it's doing
    for part in getattr(response.candidates[0].content, 'parts', []):
        if hasattr(part, 'text') and part.text:
            print(part.text)

        elif hasattr(part, 'function_call'):
            try:
                result = call_function(part.function_call, verbose_arg)
                # Validate result structure before accessing deeply nested attributes
                if (
                    not result or
                    not hasattr(result, 'parts') or
                    not result.parts or
                    not hasattr(result.parts[0], 'function_response') or
                    not hasattr(result.parts[0].function_response, 'response') or
                    not result.parts[0].function_response.response
                ):
                    raise RuntimeError("Function call did not return a valid response.")
                if verbose_arg ==True:
                    print(f"-> {result.parts[0].function_response.response}")

            except Exception as e:
                print(f"Exception occurred while processing function call: {e}")
                sys.exit(1)


if __name__ == "__main__":
    main()