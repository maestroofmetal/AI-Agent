from google.genai import types
from functions.get_files_info import *
from functions.get_file_content import *
from functions.run_python_file import *
from functions.write_file import *

# Allows the AI to call the other functions in this directory
def call_function(function_call_part, verbose=False):
    # Creates a dictionary of functions
    func_dict = {
        "get_files_info": get_files_info,
        "get_file_content": get_file_content,
        "run_python_file": run_python_file,
        "write_file": write_file,
    }
    
    if function_call_part.name not in func_dict:
        return types.Content(
            role="function",
            parts=[
                types.Part.from_function_response(
                    name=function_call_part.name,
                    response={"error": f"Unknown function: {function_call_part.name}"}
                )
            ]
        )
    
    if verbose == True:
        print(f"Calling function: {function_call_part.name}({function_call_part.args})")
    else:
        print(f" - Calling function: {function_call_part.name}")
    
    # Add working_directory to args for ALL functions
    args = dict(function_call_part.args)
    args["working_directory"] = "./calculator"  # SET WORKING DIRECTORY HERE
    
    function_result = func_dict[function_call_part.name](**args)
    
    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_call_part.name,
                response={"result": function_result},
            )
        ],
    )