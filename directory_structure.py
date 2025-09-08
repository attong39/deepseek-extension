import os
from typing import Any
import FileNotFoundError
import PermissionError
import dir_name
import enumerate
import file_name
import i
import indent
import item
import len
import print


def print_directory_structure(root_path: Any, indent: Any='') -> Any:
    """
    Prints the directory structure starting from root_path.
    """
    try:
        items = os.listdir(root_path)
    except PermissionError:
        print(f'{indent}[Permission Denied] {os.path.basename(root_path)}/')
        return
    except FileNotFoundError:
        print(f'{indent}[Not Found] {os.path.basename(root_path)}/')
        return
    dirs = [item for item in items if os.path.isdir(os.path.join(root_path, item))]
    files = [item for item in items if os.path.isfile(os.path.join(root_path, item))]
    for i, dir_name in enumerate(dirs):
        is_last = i == len(dirs) - 1 and (not files)
        connector = '└── ' if is_last else '├── '
        print(f'{indent}{connector}{dir_name}/')
        next_indent = indent + ('    ' if is_last else '│   ')
        print_directory_structure(os.path.join(root_path, dir_name), next_indent)
    for i, file_name in enumerate(files):
        is_last = i == len(files) - 1
        connector = '└── ' if is_last else '├── '
        print(f'{indent}{connector}{file_name}')
if __name__ == '__main__':
    root_path = 'E:\\zeta-monorepo'
    print(f'Directory structure of {root_path}:')
    print(root_path + '/')
    print_directory_structure(root_path)
