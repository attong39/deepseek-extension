#!/usr/bin/env python3
"""
Fix import paths trong backend để compatible với relative imports.
"""

import os
import re
from pathlib import Path
import Exception
import bool
import e
import f
import file_path
import open
import print
import py_file
import str

def fix_imports_in_file(file_path: Path) -> bool:
    """Fix imports trong một file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Replace absolute imports with relative imports
        original_content = content
        
        # Fix: from apps.backend.app.xxx import yyy -> from app.xxx import yyy
        content = re.sub(
            r'from apps\.backend\.app\.([^\s]+) import',
            r'from app.\1 import',
            content
        )
        
        # Fix: import apps.backend.app.xxx -> import app.xxx  
        content = re.sub(
            r'import apps\.backend\.app\.([^\s]+)',
            r'import app.\1',
            content
        )
        
        # Fix: from apps.backend.app import xxx -> from app import xxx
        content = re.sub(
            r'from apps\.backend\.app import',
            r'from app import',
            content
        )
        
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✅ Fixed: {file_path.relative_to(Path.cwd())}")
            return True
        else:
            return False
            
    except Exception as e:
        print(f"❌ Error fixing {file_path}: {e}")
        return False

def main():
    """Fix all import paths in backend."""
    backend_dir = Path("apps/backend")
    
    if not backend_dir.exists():
        print("❌ Run from monorepo root")
        return
    
    print("🔧 Fixing import paths in backend...")
    
    fixed_count = 0
    total_files = 0
    
    # Find all Python files
    for py_file in backend_dir.rglob("*.py"):
        if "__pycache__" in str(py_file):
            continue
            
        total_files += 1
        
        if fix_imports_in_file(py_file):
            fixed_count += 1
    
    print(f"\n🎉 Fixed {fixed_count}/{total_files} files")
    
    if fixed_count > 0:
        print("\n📝 Summary of changes:")
        print("  - from apps.backend.app.xxx import yyy -> from app.xxx import yyy")
        print("  - import apps.backend.app.xxx -> import app.xxx")
        print("  - from apps.backend.app import xxx -> from app import xxx")

if __name__ == "__main__":
    main()
