import os
import subprocess
from config import *

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Runs the given python file with the provided arguments",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the python file to be ran, relative to the working directory.",
            ),
            "args": types.Schema(
                type=types.Type.STRING,
                description="The list of arguments to be passed to be passed to the python file that is being ran.",
            ),
        },
    ),
)

def run_python_file(working_directory, file_path, args=[]):
    try:
        abs_working_directory = os.path.abspath(os.path.join("./", working_directory))
        abs_file = os.path.abspath(os.path.join(working_directory, file_path))    
    
        if os.path.commonpath([abs_working_directory]) != os.path.commonpath([abs_working_directory, abs_file]):
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(abs_file):
            return f'Error: File "{file_path}" not found.'
        if abs_file.split(".")[-1:][0] != "py":
            return f'Error: "{file_path}" is not a Python file.'
    except:
        return f"Error: Invalid file path"
    try:
        completed_process = subprocess.run(["python", abs_file] + args, timeout=30, capture_output=True, cwd=abs_working_directory)
    except Exception as e:
        return f"Error: executing Python file: {e}"
    if len(completed_process.stdout) == 0 and len(completed_process.stderr) == 0:
        return f"No output produced."
    output = f"STDOUT: {completed_process.stdout} \nSTDERR: {completed_process.stderr}"
    if completed_process.returncode != 0:
        output += f"\nProcess exited with code {completed_process.returncode}"
    return output
    