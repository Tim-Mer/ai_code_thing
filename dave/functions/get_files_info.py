import os

class dir_item:
    def __init__(self, name: str, file_size: int, is_dir: bool):
        self.name = name
        self.file_size = file_size
        self.is_dir = is_dir
    
    def __repr__(self):
        return f"- {self.name}: file_size={self.file_size} bytes, is_dir={self.is_dir}"

def get_files_info(working_directory, directory="."):
    try:
        abs_working_directory = os.path.abspath(os.path.join("./", working_directory))
        abs_directory = os.path.abspath(os.path.join(working_directory, directory))    
    
        if os.path.commonpath([abs_working_directory]) != os.path.commonpath([abs_working_directory, abs_directory]):
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        if not os.path.isdir(abs_directory):
            return f'Error: "{directory}" is not a directory'
    except:
        return f"Error: Invalid directory passed"
    
    dir_items = []
    try:
        for item in os.listdir(abs_directory):
            item_path = os.path.join(abs_directory, item)
            dir_items.append(dir_item(item, os.path.getsize(item_path), os.path.isdir(item_path)))
    except:
        return f"Error: Unable to list directory"
    
    res = ""
    for x in dir_items:
        res += f"{x}" + f"\n"
    
    return res.rstrip("\n")        