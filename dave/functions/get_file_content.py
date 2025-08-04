import os
from config import *

CHARACTER_LIMIT = 10000

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Reads a files contents up until the specified character limit.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The name and path to the file, relative to the working directory.",
            ),
        },
    ),
)

def get_file_content(working_directory, file_path):
    try:
        abs_working_directory = os.path.abspath(os.path.join("./", working_directory))
        abs_file = os.path.abspath(os.path.join(working_directory, file_path))    
    
        if os.path.commonpath([abs_working_directory]) != os.path.commonpath([abs_working_directory, abs_file]):
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(abs_file):
            return f'Error: File not found or is not a regular file: "{file_path}"'
    except:
        return f"Error: Invalid file path"
    print(f"Trying to open {abs_file}")
    try:
        with open(abs_file, "r") as f:
            content = f.read(CHARACTER_LIMIT+1)
            if len(content) > CHARACTER_LIMIT:
                content = content[:CHARACTER_LIMIT] + f'[...File "{file_path}" truncated at {CHARACTER_LIMIT} characters]'
    except Exception as e:
        return f"Error: Something went wrong reading the file {e}"
    return content