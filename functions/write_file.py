import os

def write_file(working_directory, file_path, content):
    try:
        joined = os.path.join(working_directory, file_path)
        abs_working_dir = os.path.abspath(working_directory)
        abs_joined_path = os.path.abspath(joined)
        
        #contains the AI
        if not abs_joined_path.startswith(abs_working_dir):
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        if not os.path.exists(joined):
            try:
                os.makedirs(file_path)
            except Exception as e:
                return f'Error: {e}'
        
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