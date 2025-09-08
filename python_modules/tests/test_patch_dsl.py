"""
Unit tests for the patch_dsl module.

This module contains comprehensive tests for the apply_fenced_patches and 
src_endswith_nl functions, covering various edge cases and error conditions.
"""

import unittest
import tempfile
import shutil
from pathlib import Path
from unittest.mock import patch, mock_open

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from patch_dsl import apply_fenced_patches, src_endswith_nl


class TestSrcEndsWithNl(unittest.TestCase):
    """Test cases for the src_endswith_nl function."""
    
    def setUp(self):
        """Set up test environment with temporary directory."""
        self.test_dir = Path(tempfile.mkdtemp())
    
    def tearDown(self):
        """Clean up test environment."""
        shutil.rmtree(self.test_dir)
    
    def test_file_ends_with_newline(self):
        """Test file that ends with newline character."""
        test_file = self.test_dir / "test_newline.txt"
        test_file.write_text("content\n")
        
        result = src_endswith_nl(test_file)
        self.assertTrue(result)
    
    def test_file_without_newline(self):
        """Test file that doesn't end with newline character."""
        test_file = self.test_dir / "test_no_newline.txt"
        test_file.write_text("content")
        
        result = src_endswith_nl(test_file)
        self.assertFalse(result)
    
    def test_empty_file(self):
        """Test empty file returns True."""
        test_file = self.test_dir / "test_empty.txt"
        test_file.touch()
        
        result = src_endswith_nl(test_file)
        self.assertTrue(result)
    
    def test_nonexistent_file(self):
        """Test nonexistent file returns True."""
        test_file = self.test_dir / "nonexistent.txt"
        
        result = src_endswith_nl(test_file)
        self.assertTrue(result)
    
    def test_directory_path(self):
        """Test directory path returns True."""
        result = src_endswith_nl(self.test_dir)
        self.assertTrue(result)
    
    def test_binary_file_with_newline(self):
        """Test binary file that ends with newline byte."""
        test_file = self.test_dir / "test_binary.bin"
        test_file.write_bytes(b"binary\x00data\n")
        
        result = src_endswith_nl(test_file)
        self.assertTrue(result)
    
    def test_binary_file_without_newline(self):
        """Test binary file that doesn't end with newline byte."""
        test_file = self.test_dir / "test_binary.bin"
        test_file.write_bytes(b"binary\x00data")
        
        result = src_endswith_nl(test_file)
        self.assertFalse(result)
    
    @patch('builtins.open', side_effect=PermissionError("Access denied"))
    def test_permission_error(self, mock_file):
        """Test permission error returns True."""
        test_file = Path("protected_file.txt")
        
        result = src_endswith_nl(test_file)
        self.assertTrue(result)


class TestApplyFencedPatches(unittest.TestCase):
    """Test cases for the apply_fenced_patches function."""
    
    def setUp(self):
        """Set up test environment with temporary directory."""
        self.test_dir = Path(tempfile.mkdtemp())
        # Change to test directory to work with relative paths
        self.original_cwd = os.getcwd()
        os.chdir(self.test_dir)
    
    def tearDown(self):
        """Clean up test environment."""
        os.chdir(self.original_cwd)
        shutil.rmtree(self.test_dir)
    
    def test_append_mode_dry_run(self):
        """Test append mode in dry run (apply=False)."""
        text = """```python test.py append
# This is a test comment
print("Hello, World!")
```"""
        
        result = apply_fenced_patches(text, apply=False)
        
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0], Path("test.py"))
        # File should not be created in dry run
        self.assertFalse(Path("test.py").exists())
    
    def test_append_mode_apply(self):
        """Test append mode with actual file creation."""
        text = """```python test.py append
# This is a test comment
print("Hello, World!")
```"""
        
        result = apply_fenced_patches(text, apply=True)
        
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0], Path("test.py"))
        
        # File should be created
        test_file = Path("test.py")
        self.assertTrue(test_file.exists())
        
        content = test_file.read_text()
        expected_content = "# This is a test comment\nprint(\"Hello, World!\")\n"
        self.assertEqual(content, expected_content)
    
    def test_append_to_existing_file(self):
        """Test appending to an existing file."""
        # Create initial file
        test_file = Path("existing.py")
        test_file.write_text("# Initial content\n")
        
        text = """```python existing.py append
# Appended content
```"""
        
        result = apply_fenced_patches(text, apply=True)
        
        self.assertEqual(len(result), 1)
        
        content = test_file.read_text()
        expected_content = "# Initial content\n# Appended content\n"
        self.assertEqual(content, expected_content)
    
    def test_append_to_file_without_newline(self):
        """Test appending to file that doesn't end with newline."""
        # Create initial file without ending newline
        test_file = Path("no_newline.py")
        test_file.write_text("content")
        
        text = """```python no_newline.py append
# Appended content
```"""
        
        apply_fenced_patches(text, apply=True)
        
        content = test_file.read_text()
        expected_content = "content\n# Appended content\n"
        self.assertEqual(content, expected_content)
    
    def test_overwrite_mode(self):
        """Test overwrite mode."""
        text = """```python overwrite_test.py overwrite
# This will overwrite everything
def new_function():
    pass
```"""
        
        result = apply_fenced_patches(text, apply=True)
        
        self.assertEqual(len(result), 1)
        
        test_file = Path("overwrite_test.py")
        self.assertTrue(test_file.exists())
        
        content = test_file.read_text()
        expected_content = "# This will overwrite everything\ndef new_function():\n    pass\n"
        self.assertEqual(content, expected_content)
    
    def test_replace_mode(self):
        """Test replace mode."""
        # Create initial file
        test_file = Path("replace_test.py")
        initial_content = """def old_function():
    print("old")

def keep_function():
    print("keep")
"""
        test_file.write_text(initial_content)
        
        text = """```python replace_test.py replace def old_function():\n    print("old")
def new_function():
    print("new")
```"""
        
        result = apply_fenced_patches(text, apply=True)
        
        self.assertEqual(len(result), 1)
        
        content = test_file.read_text()
        self.assertIn("def new_function():", content)
        self.assertIn("def keep_function():", content)
        self.assertNotIn("def old_function():", content)
    
    def test_multiple_patches(self):
        """Test multiple patches in one text."""
        text = """
```python file1.py append
# Content for file 1
```

```javascript file2.js overwrite
// Content for file 2
console.log("hello");
```
"""
        
        result = apply_fenced_patches(text, apply=True)
        
        self.assertEqual(len(result), 2)
        self.assertIn(Path("file1.py"), result)
        self.assertIn(Path("file2.js"), result)
        
        # Check both files were created
        self.assertTrue(Path("file1.py").exists())
        self.assertTrue(Path("file2.js").exists())
    
    def test_subdirectory_creation(self):
        """Test creating files in subdirectories."""
        text = """```python src/utils/helper.py append
def helper_function():
    return True
```"""
        
        result = apply_fenced_patches(text, apply=True)
        
        self.assertEqual(len(result), 1)
        
        # Check subdirectory was created
        test_file = Path("src/utils/helper.py")
        self.assertTrue(test_file.exists())
        self.assertTrue(test_file.parent.exists())
    
    def test_invalid_mode_error(self):
        """Test error handling for invalid mode."""
        text = """```python test.py invalid_mode
content
```"""
        
        with self.assertRaises(ValueError) as context:
            apply_fenced_patches(text, apply=True)
        
        self.assertIn("Unsupported mode 'invalid_mode'", str(context.exception))
    
    def test_replace_mode_missing_search_pattern(self):
        """Test error for replace mode without search pattern."""
        text = """```python test.py replace
new content
```"""
        
        with self.assertRaises(ValueError) as context:
            apply_fenced_patches(text, apply=True)
        
        self.assertIn("Replace mode requires a search pattern", str(context.exception))
    
    def test_replace_mode_pattern_not_found(self):
        """Test error when replace pattern is not found."""
        # Create initial file
        test_file = Path("test.py")
        test_file.write_text("existing content")
        
        text = """```python test.py replace nonexistent_pattern
new content
```"""
        
        with self.assertRaises(ValueError) as context:
            apply_fenced_patches(text, apply=True)
        
        self.assertIn("Search pattern 'nonexistent_pattern' not found", str(context.exception))
    
    def test_replace_mode_nonexistent_file(self):
        """Test error when trying to replace in nonexistent file."""
        text = """```python nonexistent.py replace old_content
new content
```"""
        
        with self.assertRaises(ValueError) as context:
            apply_fenced_patches(text, apply=True)
        
        self.assertIn("Cannot replace content in non-existent file", str(context.exception))
    
    def test_absolute_path_security(self):
        """Test that absolute paths are converted to relative."""
        text = """```python /etc/passwd append
malicious content
```"""
        
        result = apply_fenced_patches(text, apply=False)
        
        # Should convert absolute path to just the filename
        self.assertEqual(result[0], Path("passwd"))
    
    def test_path_traversal_security(self):
        """Test that path traversal attempts are blocked."""
        text = """```python ../../../etc/passwd append
malicious content
```"""
        
        with self.assertRaises(ValueError) as context:
            apply_fenced_patches(text, apply=False)
        
        self.assertIn("Path traversal detected", str(context.exception))
    
    def test_no_fenced_blocks(self):
        """Test text with no fenced blocks."""
        text = "This is just regular text with no code blocks."
        
        result = apply_fenced_patches(text, apply=True)
        
        self.assertEqual(len(result), 0)
    
    def test_malformed_fenced_block(self):
        """Test malformed fenced block doesn't cause errors."""
        text = """```
This is a malformed block without proper header
```"""
        
        result = apply_fenced_patches(text, apply=True)
        
        # Should return empty list for malformed blocks
        self.assertEqual(len(result), 0)
    
    def test_content_without_ending_newline(self):
        """Test that content without ending newline gets one added."""
        text = """```python test.py overwrite
content without newline
```"""
        
        apply_fenced_patches(text, apply=True)
        
        test_file = Path("test.py")
        content = test_file.read_text()
        self.assertTrue(content.endswith('\n'))


if __name__ == '__main__':
    unittest.main()