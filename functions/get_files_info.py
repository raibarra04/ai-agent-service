import os

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

            for item in os.listdir(dir_abs_path):
                file_abs_path = os.path.join(dir_abs_path, item)
                file_size = os.path.getsize(file_abs_path)
                is_dir = os.path.isfile(file_abs_path)
                print(f'- {item}: file-size={file_size} bytes, is_dir={is_dir}')
        return 0
    
    except Exception as e:
        print(f'Error: {str(e)}')
        return 1
