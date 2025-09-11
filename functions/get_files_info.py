import os
import sys

def get_files_info(working_directory, directory="."):
    try:
        working_abs_path = os.path.abspath(working_directory)
        combined_relative_path = os.path.join(working_directory, directory)
        dir_abs_path = os.path.abspath(combined_relative_path)

        if (not dir_abs_path.startswith(working_abs_path)):
            raise ValueError(f'Cannot list "{directory}" as it is outside the permitted working directory')
        if (not os.path.isdir(dir_abs_path)):
            raise ValueError(f'"{directory}" is not a directory')
        else:
            dir_arg = f"'{directory}'"
            if directory == '.':
                dir_arg = 'current'

            print(f"Result for {dir_arg} directory:")
            for item in os.listdir(dir_abs_path):
                file_abs_path = os.path.join(dir_abs_path, item)
                file_size = os.path.getsize(file_abs_path)
                is_dir = os.path.isfile(file_abs_path)
                print(f'   - {item}: file-size={file_size} bytes, is_dir={is_dir}')

    
    except Exception as e:
        print(f"Result for {directory} directory:")
        print(f'   Error: {str(e)}')
        return 1


get_files_info("../calculator", ".")
get_files_info("../calculator", "pkg")
get_files_info("../calculator", "/bin")
get_files_info("../calculator", "../")
get_files_info("../calculator", "wumbo")
