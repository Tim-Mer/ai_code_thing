import os
from config import *

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Creates and writes a file to the specified path with specified content",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file, relative to the working directory.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The content that is to be writen to the file.",
            ),
        },
    ),
)

def write_file(working_directory, file_path, content):
    try:
        abs_working_directory = os.path.abspath(os.path.join("./", working_directory))
        abs_file = os.path.abspath(os.path.join(working_directory, file_path))    
    
        if os.path.commonpath([abs_working_directory]) != os.path.commonpath([abs_working_directory, abs_file]):
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(abs_file):
            try:
                #os.makedirs(os.path.dirname(abs_file))
                with open(abs_file, "a") as f:
                    f.write("")
            except:
                return f'Error: Unable to create file "{file_path}"'
    except:
        return f"Error: Invalid file path"
    try:
        with open(abs_file, "w") as f:
            f.write(content)
    except:
        return f"Error: Something went wrong writing the file"
    return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'