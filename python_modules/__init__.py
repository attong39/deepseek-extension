"""
Python modules for the DeepSeek VS Code extension.

This package contains utility modules for processing code patches and 
text operations within the DeepSeek AI assistant extension.
"""

from .patch_dsl import apply_fenced_patches, src_endswith_nl

__all__ = ['apply_fenced_patches', 'src_endswith_nl']
__version__ = '1.0.0'