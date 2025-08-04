from google.genai import types
from functions.get_files_info import *
from functions.get_file_content import *
from functions.run_python import *
from functions.write_file import *

system_prompt = """
You are a helpful AI coding agent.
When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories
- Read file contents
- Execute Python files with optional arguments
- Write or overwrite files

Do not create a new file unless explecitly needed, only overwrite current files with your sugestions.

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""

def call_function(function_call_part, verbose=False):
    funcs = {
        "get_files_info": get_files_info,
        "get_file_content": get_file_content,
        "run_python_file": run_python_file,
        "write_file": write_file
    }

    function_call_part.args["working_directory"] = "./calculator/"
    if verbose:
        print(f"Calling function: {function_call_part.name}(**{function_call_part.args})")
    else:
        print(f" - Calling function: {function_call_part.name}")
    try:
        function_result = funcs[function_call_part.name](**function_call_part.args)
    except:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_call_part.name,
                    response={"error": f"Unknown function: {function_call_part.name}"},
                )
            ],
        )
    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_call_part.name,
                response={"result": function_result},
            )
        ],
    )
