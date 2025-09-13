import os
import subprocess
import copy

def run_python_file(working_directory, file_path, args=[]):
    abs_working_path = os.path.abspath(working_directory)
    abs_file_path = os.path.abspath(os.path.join(working_directory, file_path))

    if not abs_file_path.startswith(abs_working_path):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'   

    if not os.path.exists(abs_file_path):
        return f'Error: File "{file_path}" not found.'

    if not file_path.endswith('.py'):
        return f'Error: "{file_path}" is not a Python file.'
    
    try:
        args_copy = copy.deepcopy(args)
        new_args = ['python3', file_path, *args_copy]
        response = subprocess.run(
                new_args, cwd=abs_working_path, timeout=30, capture_output= True, text=True)

        if (response.stdout):
            print(f'STDOUT:\n{response.stdout}')
        if (response.stderr):
            print(f'STDERR:{response.stderr}')
        if response.returncode != 0:
            print(f'Process exited with code {response.returncode}')

    except Exception as e:
        return f"Error: executing Python file: {e}"
