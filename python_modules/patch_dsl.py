"""
Patch DSL module for processing fenced code blocks and applying file changes.

This module provides functionality to parse fenced code blocks from text input
and apply various operations (append, overwrite, replace) to specified files.
"""

import re
from pathlib import Path
from typing import List


def src_endswith_nl(p: Path) -> bool:
    """
    Check if a file ends with a newline character.
    
    This function reads the last character of a file to determine if it ends
    with a newline character. It handles various edge cases including empty
    files and file read errors.
    
    Args:
        p (Path): The path to the file to check.
    
    Returns:
        bool: True if the file ends with '\\n', False if it doesn't. Returns 
              True if the file is empty or if there's an error reading the file.
    
    Raises:
        None: This function handles all exceptions internally and returns a 
              boolean value in all cases.
    
    Examples:
        >>> from pathlib import Path
        >>> src_endswith_nl(Path("file_with_newline.txt"))
        True
        >>> src_endswith_nl(Path("file_without_newline.txt"))
        False
    """
    try:
        if not p.exists() or not p.is_file():
            return True
        
        # Read the last character of the file
        with p.open('rb') as f:
            # For empty files, consider them as ending with newline
            if f.seek(0, 2) == 0:  # Seek to end, get size
                return True
            
            # Go back one character from the end
            f.seek(-1, 2)
            last_char = f.read(1)
            return last_char == b'\n'
    
    except (OSError, IOError, PermissionError):
        # Return True for any file access errors as a safe default
        return True


def apply_fenced_patches(text: str, apply: bool) -> List[Path]:
    """
    Apply patch operations from fenced code blocks in the input text.
    
    This function parses text containing fenced code blocks with special headers
    that specify file operations. It supports three modes: append, overwrite, 
    and replace operations on files.
    
    Expected fenced code block format:
    ```language path/to/file.ext mode [search_pattern]
    content to be applied
    ```
    
    Supported modes:
    - 'append': Append content to the end of the file
    - 'overwrite': Replace entire file content
    - 'replace': Replace specific content (requires search pattern)
    
    Args:
        text (str): Input text containing fenced code blocks with patch instructions.
        apply (bool): If True, actually apply the changes to files. If False, 
                     perform a dry run and return the list of files that would be modified.
    
    Returns:
        List[Path]: List of Path objects representing files that were modified 
                   (or would be modified in dry-run mode).
    
    Raises:
        ValueError: If a path is invalid, mode is not supported, or header format is incorrect.
        OSError: If there are file permission or access issues during file operations.
    
    Examples:
        >>> text = '''```python src/example.py append
        ... # This comment will be appended
        ... ```'''
        >>> files = apply_fenced_patches(text, apply=False)
        >>> len(files)
        1
        >>> str(files[0])
        'src/example.py'
    """
    # Regular expression to match fenced code blocks with headers
    # Updated pattern to capture any mode, then validate it
    fence_pattern = re.compile(
        r'```(?P<language>\w*)\s+(?P<path>\S+)\s+(?P<mode>\w+)(?P<extra_args>.*?)\n'
        r'(?P<content>.*?)\n```',
        re.DOTALL | re.MULTILINE
    )
    
    modified_files = []
    
    for match in fence_pattern.finditer(text):
        language = match.group('language')
        path_str = match.group('path')
        mode = match.group('mode')
        extra_args = match.group('extra_args').strip() if match.group('extra_args') else ''
        content = match.group('content')
        
        # For replace mode, extract search pattern from extra_args
        search_pattern = extra_args if mode == 'replace' else None
        
        # Validate path
        try:
            file_path = Path(path_str)
            if file_path.is_absolute():
                # For security, convert absolute paths to relative
                # Keep only the filename for absolute paths
                file_path = Path(file_path.name)
        except (ValueError, OSError) as e:
            raise ValueError(f"Invalid path '{path_str}': {e}")
        
        # Validate mode
        if mode not in ['append', 'overwrite', 'replace']:
            raise ValueError(f"Unsupported mode '{mode}'. Supported modes: append, overwrite, replace")
        
        # For replace mode, search pattern is required
        if mode == 'replace' and not search_pattern:
            raise ValueError(f"Replace mode requires a search pattern for file '{path_str}'")
        
        # Add to modified files list
        modified_files.append(file_path)
        
        # If not applying, skip the actual file operations
        if not apply:
            continue
        
        try:
            # Ensure parent directory exists
            file_path.parent.mkdir(parents=True, exist_ok=True)
            
            if mode == 'append':
                # Check if file needs a newline before appending
                needs_newline = False
                if file_path.exists() and not src_endswith_nl(file_path):
                    needs_newline = True
                
                with file_path.open('a', encoding='utf-8') as f:
                    if needs_newline:
                        f.write('\n')
                    f.write(content)
                    # Ensure the appended content ends with a newline
                    if not content.endswith('\n'):
                        f.write('\n')
            
            elif mode == 'overwrite':
                with file_path.open('w', encoding='utf-8') as f:
                    f.write(content)
                    # Ensure the file ends with a newline
                    if not content.endswith('\n'):
                        f.write('\n')
            
            elif mode == 'replace':
                if not file_path.exists():
                    raise ValueError(f"Cannot replace content in non-existent file '{path_str}'")
                
                # Read current content
                with file_path.open('r', encoding='utf-8') as f:
                    current_content = f.read()
                
                # Perform replacement
                if search_pattern not in current_content:
                    raise ValueError(f"Search pattern '{search_pattern}' not found in file '{path_str}'")
                
                new_content = current_content.replace(search_pattern, content)
                
                # Write back the modified content
                with file_path.open('w', encoding='utf-8') as f:
                    f.write(new_content)
        
        except (OSError, IOError, PermissionError) as e:
            raise OSError(f"Error processing file '{path_str}': {e}")
    
    return modified_files