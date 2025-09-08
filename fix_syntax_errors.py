from typing import Any
import Exception
import SyntaxError
import UnicodeDecodeError
import any
import bool
import directory
import e
import enumerate
import error_msg
import f
import file_path
import filename
import filenames
import has_error
import i
import j
import k
import len
import list
import min
import open
import print
import range
import root
import skip
import str
import tuple

"""Fix syntax errors across the project."""
import ast
import os
import re


def find_python_files(directory: str) -> list[str]:
    """Find all Python files in directory."""
    files = []
    for root, dirs, filenames in os.walk(directory):
        if any(skip in root for skip in ['.git', '__pycache__', '.pytest_cache', 'node_modules', '.venv', 'venv']):
            continue
        for filename in filenames:
            if filename.endswith('.py'):
                files.append(os.path.join(root, filename))
    return files

def check_syntax_error(file_path: str) -> tuple[bool, str]:
    """Check if file has syntax error."""
    try:
        with open(file_path, encoding='utf-8') as f:
            content = f.read()
        ast.parse(content)
        return (False, '')
    except SyntaxError as e:
        return (True, str(e))
    except UnicodeDecodeError:
        return (True, 'Unicode decode error')
    except Exception as e:
        return (True, str(e))

def fix_common_syntax_errors(file_path: str) -> bool:
    """Fix common syntax errors."""
    try:
        with open(file_path, encoding='utf-8') as f:
            content = f.read()
        original_content = content
        lines = content.split('\n')
        fixed_lines = []
        for i, line in enumerate(lines):
            if (line.strip().startswith('import ') or line.strip().startswith('from ')) and i > 0:
                if line.startswith('        '):
                    line = line[8:]
                elif line.startswith('    '):
                    if not (lines[i - 1].strip().endswith('(') or lines[i - 1].strip().endswith('\\')):
                        line = line[4:]
            if line.strip() == 'from typing import (':
                for j in range(i + 1, min(i + 10, len(lines))):
                    if ')' in lines[j]:
                        imports = []
                        for k in range(i + 1, j):
                            if lines[k].strip() and (not lines[k].strip().startswith('#')):
                                imports.append(lines[k].strip().rstrip(','))
                        if imports:
                            line = f"from typing import {', '.join(imports)}"
                            for k in range(i + 1, j + 1):
                                if k < len(lines):
                                    lines[k] = ''
                        break
            if '= lambda' in line and ': lambda' not in line:
                pass
            fixed_lines.append(line)
        content = '\n'.join(fixed_lines)
        content = re.sub('\\n\\s*\\n\\s*\\n', '\n\n', content)
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        return False
    except Exception as e:
        print(f'Error fixing {file_path}: {e}')
        return False

def main() -> Any:
    """Main function."""
    print('🔍 Finding Python files...')
    python_files = find_python_files('.')
    print(f'Found {len(python_files)} Python files')
    print('\n🔍 Checking for syntax errors...')
    syntax_errors = []
    for file_path in python_files:
        has_error, error_msg = check_syntax_error(file_path)
        if has_error:
            syntax_errors.append((file_path, error_msg))
    if not syntax_errors:
        print('✅ No syntax errors found!')
        return
    print(f'\n❌ Found {len(syntax_errors)} files with syntax errors:')
    for file_path, error_msg in syntax_errors:
        print(f'  - {file_path}: {error_msg}')
    print('\n🔧 Attempting to fix syntax errors...')
    fixed_count = 0
    for file_path, error_msg in syntax_errors:
        print(f'Fixing {file_path}...')
        if fix_common_syntax_errors(file_path):
            has_error, _ = check_syntax_error(file_path)
            if not has_error:
                print(f'  ✅ Fixed: {file_path}')
                fixed_count += 1
            else:
                print(f'  ❌ Still has errors: {file_path}')
        else:
            print(f'  ⚠️  No changes made: {file_path}')
    print(f'\n📊 Summary: Fixed {fixed_count}/{len(syntax_errors)} files')
    remaining_errors = []
    for file_path, _ in syntax_errors:
        has_error, error_msg = check_syntax_error(file_path)
        if has_error:
            remaining_errors.append((file_path, error_msg))
    if remaining_errors:
        print(f'\n⚠️  {len(remaining_errors)} files still have syntax errors:')
        for file_path, error_msg in remaining_errors:
            print(f'  - {file_path}: {error_msg}')
if __name__ == '__main__':
    main()
