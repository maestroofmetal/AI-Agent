import os
from config import MAX_CHARS
from google.genai import types

def get_file_content(working_directory, file_path):
    try:
        joined = os.path.join(working_directory, file_path)
        abs_working_dir = os.path.abspath(working_directory)
        abs_joined_path = os.path.abspath(joined)
        
        # Contains the AI
        if not abs_joined_path.startswith(abs_working_dir):
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        if os.path.isfile(joined) == False:
            return f'Error: File not found or is not a regular file: "{file_path}"'
        if os.path.isfile(joined):
            # Opens the target file
            try:
                with open(joined, "r", encoding="utf-8") as file:
                    file_content = file.read()
                    if len(file_content) > MAX_CHARS:
                        file_content = file_content [:MAX_CHARS] + f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
            except UnicodeDecodeError:
                with open(joined, "r", encoding="latin-1") as file: #fallback encoding
                    file_content = file.read()
                    if len(file_content) > MAX_CHARS:
                        file_content = file_content [:MAX_CHARS] + f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
    except Exception as e:
        return f'Error: {e}'
    return file_content

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Retrieves and reads content in a specified file.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)