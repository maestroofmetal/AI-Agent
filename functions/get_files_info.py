import os
from google.genai import types

def get_files_info(working_directory, directory="."):
    # Contains the AI
    try:
        joined = os.path.join(working_directory, directory)
        abs_working_dir = os.path.abspath(working_directory)
        abs_joined_path = os.path.abspath(joined)
        if directory == ".":
            header = "Result for current directory:\n"
        else:
            header = f"Result for {repr(directory)} directory:\n"
        
        # Contains the AI
        if not abs_joined_path.startswith(abs_working_dir):
            return f'{header}    Error: Cannot list "{directory}" as it is outside the permitted working directory'
        if os.path.isdir(joined) == False:
            return f'{header}    Error: "{directory}" is not a directory'
        
        dir_contents = os.listdir(joined)
        file_data = []
        for file in dir_contents:
            file_path = os.path.join(joined, file)
            info = \
                f"- {file}: file_size={os.path.getsize(file_path)} bytes, " \
                f"is_dir={os.path.isdir(file_path)}"
            file_data.append(info)
        content_string = f'{header}{"\n".join(file_data)}'
    except Exception as e:
        return f"Error: {e}"
        
    return content_string

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)