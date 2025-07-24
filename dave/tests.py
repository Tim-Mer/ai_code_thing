from functions import get_files_info

test_list = [".", "pkg", "/bin", "../"]

for item in test_list:
    print(f"Result for '{item}' directory")
    print(get_files_info.get_files_info("calculator", item))

