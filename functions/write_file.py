import os
from google.genai import types

def write_file(working_directory, file_path, content):
    try:
        joined = os.path.join(working_directory, file_path)
        abs_working_dir = os.path.abspath(working_directory)
        abs_joined_path = os.path.abspath(joined)
        
        #contains the AI
        if not abs_joined_path.startswith(abs_working_dir):
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        # Create directory if it doesn't exist
        directory = os.path.dirname(joined)
        if directory and not os.path.exists(directory):
            try:
                os.makedirs(directory)
            except Exception as e:
                return f'Error creating directory: {e}'
        
        # opens the file for writing
        try:
            with open(joined, "w", encoding="utf-8") as file:
                file.write(content)
                return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
        except UnicodeDecodeError:
            with open(joined, "w", encoding="latin-1") as file:
                file.write(content)
                return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        return "Error: {e}"
    
schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes content to a specified file.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file path to write to, relative to the working directory.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The content to write to the file.",
            ),
        },
        required=["file_path", "content"],
    ),
)