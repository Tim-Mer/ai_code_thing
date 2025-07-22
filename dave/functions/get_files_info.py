import os

def get_files_info(working_directory, directory="."):
    working_directory = os.path.abspath(os.path.join("./", working_directory))
    directory = os.path.abspath(os.path.join(working_directory, directory))    
    
    
    if os.path.commonpath([working_directory]) != os.path.commonpath([working_directory, directory]):
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    if not os.path.isdir(directory):
        return f'Error: "{directory}" is not a directory'

    
    