"""
Patch DSL module for processing fenced code blocks and applying file changes.

This module provides functionality to parse fenced code blocks from text input
and apply various operations (append, overwrite, replace) to specified files.
"""

import re
from pathlib import Path
from typing import List, Optional
from functools import lru_cache


def src_endswith_nl(p: Path) -> bool:
    """
    Check if a file ends with a newline character.
    
    This function efficiently checks the last character of a file to determine 
    if it ends with a newline character. It handles various edge cases including 
    empty files and file read errors.
    
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
        
        # Get file size for optimization
        file_size = p.stat().st_size
        if file_size == 0:
            return True
            
        # Only read the last byte for efficiency
        with p.open('rb') as f:
            f.seek(-1, 2)  # Seek to last byte
            last_byte = f.read(1)
            return last_byte == b'\n'
    
    except (OSError, IOError, PermissionError, ValueError):
        # Return True for any file access errors as a safe default
        return True


# Pre-compiled regex pattern for better performance
@lru_cache(maxsize=1)
def _get_fence_pattern() -> re.Pattern:
    """
    Get the compiled regex pattern for fenced code blocks.
    
    This pattern is cached to avoid recompilation on every function call.
    
    Returns:
        re.Pattern: Compiled regex pattern for matching fenced code blocks.
    """
    return re.compile(
        r'```(?P<language>\w*)\s+(?P<path>\S+)\s+(?P<mode>\w+)(?P<extra_args>.*?)\n'
        r'(?P<content>.*?)\n```',
        re.DOTALL | re.MULTILINE
    )


def _validate_and_sanitize_path(path_str: str) -> Path:
    """
    Validate and sanitize a file path for security.
    
    Args:
        path_str (str): The path string to validate.
    
    Returns:
        Path: A sanitized Path object.
    
    Raises:
        ValueError: If the path is invalid.
    """
    try:
        file_path = Path(path_str)
        
        # Security: Convert absolute paths to relative (use only filename)
        if file_path.is_absolute():
            file_path = Path(file_path.name)
        
        # Security: Remove any parent directory traversal attempts
        if '..' in file_path.parts:
            raise ValueError(f"Path traversal detected in '{path_str}'")
            
        return file_path
        
    except (ValueError, OSError) as e:
        raise ValueError(f"Invalid path '{path_str}': {e}")


def _write_content_with_newline(file_path: Path, content: str, mode: str = 'w') -> None:
    """
    Write content to a file ensuring it ends with a newline.
    
    Args:
        file_path (Path): Path to the file to write.
        content (str): Content to write.
        mode (str): File open mode ('w' for write, 'a' for append).
    """
    with file_path.open(mode, encoding='utf-8') as f:
        f.write(content)
        if not content.endswith('\n'):
            f.write('\n')
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
    # Use cached compiled regex pattern
    fence_pattern = _get_fence_pattern()
    
    modified_files = []
    
    for match in fence_pattern.finditer(text):
        language = match.group('language')
        path_str = match.group('path')
        mode = match.group('mode')
        extra_args = match.group('extra_args').strip() if match.group('extra_args') else ''
        content = match.group('content')
        
        # For replace mode, extract search pattern from extra_args
        search_pattern = extra_args if mode == 'replace' else None
        
        # Validate and sanitize path
        file_path = _validate_and_sanitize_path(path_str)
        
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
                _handle_append_mode(file_path, content)
            elif mode == 'overwrite':
                _write_content_with_newline(file_path, content, 'w')
            elif mode == 'replace':
                _handle_replace_mode(file_path, content, search_pattern, path_str)
        
        except (OSError, IOError, PermissionError) as e:
            raise OSError(f"Error processing file '{path_str}': {e}")
    
    return modified_files


def _handle_append_mode(file_path: Path, content: str) -> None:
    """
    Handle append mode operation.
    
    Args:
        file_path (Path): Path to the file to append to.
        content (str): Content to append.
    """
    # Check if file needs a newline before appending
    needs_newline = file_path.exists() and not src_endswith_nl(file_path)
    
    with file_path.open('a', encoding='utf-8') as f:
        if needs_newline:
            f.write('\n')
        f.write(content)
        # Ensure the appended content ends with a newline
        if not content.endswith('\n'):
            f.write('\n')


def _handle_replace_mode(file_path: Path, content: str, search_pattern: str, path_str: str) -> None:
    """
    Handle replace mode operation.
    
    Args:
        file_path (Path): Path to the file to modify.
        content (str): New content to replace with.
        search_pattern (str): Pattern to search for and replace.
        path_str (str): Original path string for error messages.
    
    Raises:
        ValueError: If file doesn't exist or pattern not found.
    """
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