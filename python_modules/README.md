# Python Modules for DeepSeek Extension

This directory contains Python modules that provide utility functions for the DeepSeek VS Code extension.

## Modules

### `patch_dsl.py`

Contains functions for processing fenced code blocks and applying file operations:

- `apply_fenced_patches(text: str, apply: bool) -> List[Path]`: Processes text containing fenced code blocks and applies file operations (append, overwrite, replace)
- `src_endswith_nl(p: Path) -> bool`: Utility function to check if a file ends with a newline character

#### Usage Example

```python
from python_modules.patch_dsl import apply_fenced_patches

text = '''```python src/example.py append
# This comment will be appended to the file
print("Hello, World!")
```'''

# Dry run - see what files would be modified
files = apply_fenced_patches(text, apply=False)
print(f"Would modify: {files}")

# Actually apply the patches
files = apply_fenced_patches(text, apply=True)
print(f"Modified: {files}")
```

#### Supported Fenced Block Format

```
```language path/to/file.ext mode [search_pattern]
content to be applied
```
```

**Modes:**
- `append`: Append content to the end of the file
- `overwrite`: Replace entire file content
- `replace`: Replace specific content (requires search_pattern)

## Testing

Run the unit tests with:

```bash
cd python_modules
python -m pytest tests/ -v
```

Or with the standard unittest module:

```bash
cd python_modules
python -m unittest tests.test_patch_dsl -v
```

## Type Checking

The code includes comprehensive type hints compatible with Python 3.7+. You can run type checking with mypy:

```bash
mypy python_modules/
```