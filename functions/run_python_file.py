import os
import subprocess
from google.genai import types

def run_python_file(working_directory, file_path, args=[]):
    try:
        joined = os.path.join(working_directory, file_path)
        abs_working_dir = os.path.abspath(working_directory)
        abs_joined_path = os.path.abspath(joined)
        
        # Contains the AI
        if not abs_joined_path.startswith(abs_working_dir):
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        if os.path.isfile(joined) == False:
            return f'Error: File "{file_path}" not found.'
        if not abs_joined_path.endswith(".py"):
            return f'Error: {file_path} is not a Python file.'
    
        # Runs the file
        result = subprocess.run(
            ["python", file_path] + args,
            timeout=30,
            capture_output=True,
            text=True,
            cwd=working_directory)
        stdout = result.stdout.strip()
        stderr = result.stderr.strip()
        output = f'STDOUT: {stdout}\nSTDERR: {stderr}'
        if result.stdout == "" and result.stderr == "":
            return "No output produced."
        if result.returncode == 0:
            return output
        elif result.returncode != 0:
            return f'''{output}
        Process exited with code {result.returncode}'''

    except Exception as e:
        return(f"Error: executing Python file: {e}")

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Runs specified file.",
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