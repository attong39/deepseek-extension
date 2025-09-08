#!/usr/bin/env python3
"""
ZETA AI SERVER - FAST DUPLICATE CODE CHECKER
Fast version that focuses on common duplicate patterns.
"""

import hashlib
import os
import re
from collections import defaultdict
from pathlib import Path
import Exception
import d
import data
import directory
import dirs
import e
import enumerate
import error
import f
import file
import file_info
import file_path
import files
import func
import i
import len
import line
import list
import loc
import locations
import open
import pattern_hash
import print
import root
import signature
import sorted
import str
import sum


def get_python_files(directory):
    """Get all Python files recursively."""
    python_files = []
    for root, dirs, files in os.walk(directory):
        # Skip certain directories for speed
        dirs[:] = [d for d in dirs if d not in [".git", "__pycache__", ".pytest_cache", "node_modules", ".venv"]]

        for file in files:
            if file.endswith(".py"):
                python_files.append(os.path.join(root, file))
    return python_files


def extract_function_signatures(content):
    """Extract function signatures and simple patterns."""
    functions = []
    imports = []
    classes = []

    lines = content.split("\n")
    for i, line in enumerate(lines):
        stripped = line.strip()

        # Function definitions
        if stripped.startswith("def "):
            # Get function signature
            func_match = re.match(r"def\s+(\w+)\s*\([^)]*\)", stripped)
            if func_match:
                functions.append({"name": func_match.group(1), "signature": stripped, "line": i + 1})

        # Class definitions
        elif stripped.startswith("class "):
            class_match = re.match(r"class\s+(\w+)", stripped)
            if class_match:
                classes.append({"name": class_match.group(1), "line": i + 1})

        # Import statements
        elif stripped.startswith(("import ", "from ")):
            imports.append(stripped)

    return functions, classes, imports


def find_duplicate_functions(files_data):
    """Find duplicate function signatures."""
    func_signatures = defaultdict(list)

    for file_path, data in files_data.items():
        for func in data["functions"]:
            # Normalize signature for comparison
            sig = re.sub(r"\s+", " ", func["signature"]).strip()
            func_signatures[sig].append({"file": file_path, "name": func["name"], "line": func["line"]})

    # Find duplicates
    duplicates = {}
    for sig, locations in func_signatures.items():
        if len(locations) > 1:
            duplicates[sig] = locations

    return duplicates


def find_similar_imports(files_data):
    """Find files with very similar import patterns."""
    import_patterns = defaultdict(list)

    for file_path, data in files_data.items():
        # Create a hash of import pattern
        imports_str = "\n".join(sorted(data["imports"]))
        import_hash = hashlib.md5(imports_str.encode()).hexdigest()[:10]
        import_patterns[import_hash].append({"file": file_path, "imports": data["imports"]})

    # Find similar patterns
    similar = {}
    for pattern_hash, files in import_patterns.items():
        if len(files) > 1:
            similar[pattern_hash] = files

    return similar


def analyze_project_fast(project_path):
    """Fast analysis focusing on obvious duplicates."""
    print(f"🚀 FAST DUPLICATE ANALYSIS - {project_path}")
    print("=" * 60)

    # Get all Python files
    print("📁 Scanning Python files...")
    python_files = get_python_files(project_path)
    print(f"📝 Found {len(python_files)} Python files")

    # Process files
    files_data = {}
    error_files = []

    print("🔍 Extracting patterns...")
    for i, file_path in enumerate(python_files):
        if i % 50 == 0:
            print(f"   Processing {i}/{len(python_files)}...")

        try:
            with open(file_path, encoding="utf-8") as f:
                content = f.read()

            functions, classes, imports = extract_function_signatures(content)
            files_data[file_path] = {
                "functions": functions,
                "classes": classes,
                "imports": imports,
            }

        except Exception as e:
            error_files.append((file_path, str(e)))

    print(f"✅ Processed {len(files_data)} files successfully")
    if error_files:
        print(f"⚠️  Skipped {len(error_files)} files due to errors")

    # Find duplicates
    print("\n🔍 Finding duplicate functions...")
    duplicate_functions = find_duplicate_functions(files_data)

    print("🔍 Finding similar import patterns...")
    similar_imports = find_similar_imports(files_data)

    # Report results
    print("\n" + "=" * 60)
    print("📊 ANALYSIS RESULTS")
    print("=" * 60)

    # Duplicate functions
    if duplicate_functions:
        print(f"\n🔄 DUPLICATE FUNCTIONS FOUND: {len(duplicate_functions)}")
        print("-" * 40)
        for i, (signature, locations) in enumerate(duplicate_functions.items()):
            if i >= 10:  # Limit output
                print(f"... and {len(duplicate_functions) - 10} more")
                break

            print(f"\n{i + 1}. {signature}")
            for loc in locations:
                rel_path = os.path.relpath(loc["file"], project_path)
                print(f"   📁 {rel_path}:{loc['line']}")
    else:
        print("\n✅ No duplicate function signatures found")

    # Similar imports
    if similar_imports:
        print(f"\n📦 SIMILAR IMPORT PATTERNS: {len(similar_imports)}")
        print("-" * 40)
        for i, (pattern_hash, files) in enumerate(similar_imports.items()):
            if i >= 5:  # Limit output
                print(f"... and {len(similar_imports) - 5} more patterns")
                break

            print(f"\n{i + 1}. Pattern {pattern_hash} ({len(files)} files):")
            for file_info in files:
                rel_path = os.path.relpath(file_info["file"], project_path)
                print(f"   📁 {rel_path}")
    else:
        print("\n✅ No similar import patterns found")

    # Summary statistics
    total_functions = sum(len(data["functions"]) for data in files_data.values())
    total_classes = sum(len(data["classes"]) for data in files_data.values())

    print("\n📈 PROJECT STATISTICS")
    print("-" * 40)
    print(f"📁 Files analyzed: {len(files_data)}")
    print(f"🔧 Total functions: {total_functions}")
    print(f"🏗️  Total classes: {total_classes}")
    print(f"🔄 Duplicate function signatures: {len(duplicate_functions)}")
    print(f"📦 Similar import patterns: {len(similar_imports)}")

    if error_files:
        print(f"\n⚠️  ERROR FILES ({len(error_files)}):")
        for file_path, error in error_files[:5]:
            rel_path = os.path.relpath(file_path, project_path)
            print(f"   ❌ {rel_path}: {error}")
        if len(error_files) > 5:
            print(f"   ... and {len(error_files) - 5} more")


if __name__ == "__main__":
    project_path = Path(__file__).parent.parent / "zeta_vn"
    analyze_project_fast(str(project_path))
