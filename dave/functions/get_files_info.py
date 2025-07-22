import os

def get_files_info(working_directory, directory="."):
    if os.path.abspath(directory) not in os.path.join(working_directory):
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    
    