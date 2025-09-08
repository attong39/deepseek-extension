#!/usr/bin/env python3
"""
prepare_vn_dataset.py - Vietnamese Python Dataset Preparation for LoRA Fine-tuning

Creates a JSONL dataset with ~150k Vietnamese-Python code samples for fine-tuning
the DeepSeek Coder model to understand Vietnamese comments and documentation.

Usage:
    python prepare_vn_dataset.py /path/to/your/project

Output:
    vn_python_dataset.jsonl - Training dataset in JSONL format
"""

import ast
import json
import logging
import os
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any
import Exception
import any
import bool
import char
import complexity
import count
import dict
import e
import enumerate
import f
import file_path
import func_info
import hasattr
import instruction
import isinstance
import len
import list
import node
import open
import output_path
import pattern
import print
import py_file
import self
import str
import template
import text
import variation
import x

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


@dataclass
class CodeSample:
    """Represents a code sample with Vietnamese context"""

    instruction: str
    input: str
    output: str
    language: str = "python"
    complexity: str = "medium"


class VietnameseDatasetGenerator:
    """Generates Vietnamese Python dataset for LoRA fine-tuning"""

    def __init__(self, project_path: str):
        self.project_path = Path(project_path)
        self.samples = []
        self.vietnamese_patterns = [
            r"#.*[àáạảãâầấậẩẫăằắặẳẵèéẹẻẽêềếệểễìíịỉĩòóọỏõôồốộổỗơờớợởỡùúụủũưừứựửữỳýỵỷỹđ]",
            r'""".*[àáạảãâầấậẩẫăằắặẳẵèéẹẻẽêềếệểễìíịỉĩòóọỏõôồốộổỗơờớợởỡùúụủũưừứựửữỳýỵỷỹđ].*"""',
            r"'''.*[àáạảãâầấậẩẫăằắặẳẵèéẹẻẽêềếệểễìíịỉĩòóọỏõôồốộổỗơờớợởỡùúụủũưừứựửữỳýỵỷỹđ].*'''",
        ]

    def is_vietnamese_text(self, text: str) -> bool:
        """Check if text contains Vietnamese characters"""
        vietnamese_chars = "àáạảãâầấậẩẫăằắặẳẵèéẹẻẽêềếệểễìíịỉĩòóọỏõôồốộổỗơờớợởỡùúụủũưừứựửữỳýỵỷỹđ"
        return any(char in vietnamese_chars for char in text.lower())

    def extract_functions_with_vn_comments(self, file_path: Path) -> list[dict[str, Any]]:
        """Extract Python functions that have Vietnamese comments/docstrings"""
        try:
            with open(file_path, encoding="utf-8") as f:
                content = f.read()

            # Parse the AST
            tree = ast.parse(content)
            functions = []

            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    # Get function source
                    start_line = node.lineno - 1
                    end_line = node.end_lineno if hasattr(node, "end_lineno") else start_line + 10

                    lines = content.split("\n")
                    if end_line > len(lines):
                        end_line = len(lines)

                    func_source = "\n".join(lines[start_line:end_line])

                    # Check for Vietnamese comments/docstrings
                    has_vietnamese = False
                    for pattern in self.vietnamese_patterns:
                        if re.search(pattern, func_source, re.DOTALL | re.IGNORECASE):
                            has_vietnamese = True
                            break

                    if has_vietnamese:
                        # Extract docstring if exists
                        docstring = ast.get_docstring(node) or ""

                        functions.append(
                            {
                                "name": node.name,
                                "source": func_source,
                                "docstring": docstring,
                                "file": str(file_path),
                                "has_vietnamese": True,
                            }
                        )

            return functions

        except Exception as e:
            logger.warning(f"Error parsing {file_path}: {e}")
            return []

    def generate_instruction_variants(self, func_info: dict[str, Any]) -> list[CodeSample]:
        """Generate multiple instruction variants for a function"""
        variants = []
        func_name = func_info["name"]
        source = func_info["source"]
        docstring = func_info["docstring"]

        # Base instruction templates in Vietnamese
        templates = [
            f"Viết hàm Python tên '{func_name}' để thực hiện chức năng như trong mô tả.",
            f"Tạo function {func_name} trong Python với logic phù hợp.",
            f"Implement hàm {func_name} bằng Python theo yêu cầu.",
            f"Code hàm {func_name} trong Python với các tính năng cần thiết.",
            f"Xây dựng function {func_name} để giải quyết vấn đề được mô tả.",
        ]

        # Enhanced templates based on function characteristics
        if "return" in source.lower():
            templates.append(f"Viết hàm {func_name} trả về kết quả như mong muốn.")

        if "def " in source and "(" in source:
            # Extract parameters
            try:
                params_match = re.search(r"def\s+\w+\s*\((.*?)\):", source)
                if params_match:
                    params = params_match.group(1).strip()
                    if params:
                        templates.append(f"Tạo hàm {func_name} nhận tham số ({params}) và xử lý dữ liệu.")
            except:
                pass

        # Generate samples
        for i, template in enumerate(templates[:3]):  # Limit to 3 variants per function
            input_context = ""
            if docstring and self.is_vietnamese_text(docstring):
                input_context = f"Mô tả: {docstring[:200]}..."

            sample = CodeSample(
                instruction=template,
                input=input_context,
                output=source,
                complexity="medium" if len(source) < 500 else "high",
            )
            variants.append(sample)

        return variants

    def generate_synthetic_samples(self) -> list[CodeSample]:
        """Generate synthetic Vietnamese Python samples"""
        synthetic_samples = []

        # Common Python patterns with Vietnamese instructions
        patterns = [
            {
                "instruction": "Viết hàm tính tổng của một danh sách số nguyên",
                "input": "Tham số: numbers (list) - danh sách các số nguyên",
                "output": '''def tinh_tong(numbers):
    """Tính tổng các số trong danh sách
    
    Args:
        numbers (list): Danh sách các số nguyên
        
    Returns:
        int: Tổng của tất cả các số
    """
    return sum(numbers)''',
            },
            {
                "instruction": "Tạo hàm kiểm tra số nguyên tố",
                "input": "Tham số: n (int) - số cần kiểm tra",
                "output": '''def la_so_nguyen_to(n):
    """Kiểm tra xem một số có phải số nguyên tố không
    
    Args:
        n (int): Số cần kiểm tra
        
    Returns:
        bool: True nếu là số nguyên tố, False nếu không
    """
    if n < 2:
        return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True''',
            },
            {
                "instruction": "Viết hàm sắp xếp danh sách theo thứ tự tăng dần",
                "input": "Tham số: arr (list) - danh sách cần sắp xếp",
                "output": '''def sap_xep_tang_dan(arr):
    """Sắp xếp danh sách theo thứ tự tăng dần
    
    Args:
        arr (list): Danh sách cần sắp xếp
        
    Returns:
        list: Danh sách đã được sắp xếp
    """
    return sorted(arr)''',
            },
            {
                "instruction": "Tạo hàm tìm phần tử lớn nhất trong danh sách",
                "input": "Tham số: data (list) - danh sách dữ liệu",
                "output": '''def tim_gia_tri_lon_nhat(data):
    """Tìm giá trị lớn nhất trong danh sách
    
    Args:
        data (list): Danh sách dữ liệu
        
    Returns:
        any: Giá trị lớn nhất trong danh sách
    """
    if not data:
        return None
    return max(data)''',
            },
            {
                "instruction": "Viết hàm đếm số lần xuất hiện của một phần tử",
                "input": "Tham số: lst (list), item (any) - danh sách và phần tử cần đếm",
                "output": '''def dem_so_lan_xuat_hien(lst, item):
    """Đếm số lần xuất hiện của một phần tử trong danh sách
    
    Args:
        lst (list): Danh sách dữ liệu
        item (any): Phần tử cần đếm
        
    Returns:
        int: Số lần xuất hiện của phần tử
    """
    return lst.count(item)''',
            },
        ]

        for pattern in patterns:
            sample = CodeSample(
                instruction=pattern["instruction"],
                input=pattern["input"],
                output=pattern["output"],
                complexity="medium",
            )
            synthetic_samples.append(sample)

        # Generate variants of each pattern
        extended_samples = []
        for sample in synthetic_samples:
            # Original sample
            extended_samples.append(sample)

            # Create variations
            variations = [
                f"Implement {sample.instruction.lower()}",
                f"Code để {sample.instruction.lower()}",
                f"Xây dựng {sample.instruction.lower()}",
                f"Tạo function để {sample.instruction.lower()}",
            ]

            for variation in variations[:2]:  # Limit variations
                variant = CodeSample(
                    instruction=variation, input=sample.input, output=sample.output, complexity=sample.complexity
                )
                extended_samples.append(variant)

        return extended_samples

    def scan_project(self) -> None:
        """Scan project for Python files with Vietnamese content"""
        logger.info(f"Scanning project: {self.project_path}")

        python_files = list(self.project_path.rglob("*.py"))
        logger.info(f"Found {len(python_files)} Python files")

        total_functions = 0
        vn_functions = 0

        for py_file in python_files:
            if "__pycache__" in str(py_file) or ".git" in str(py_file):
                continue

            functions = self.extract_functions_with_vn_comments(py_file)
            total_functions += len(functions)

            for func_info in functions:
                vn_functions += 1
                variants = self.generate_instruction_variants(func_info)
                self.samples.extend(variants)

        logger.info(f"Extracted {vn_functions} Vietnamese functions from {total_functions} total functions")

        # Add synthetic samples
        synthetic = self.generate_synthetic_samples()
        self.samples.extend(synthetic)
        logger.info(f"Added {len(synthetic)} synthetic samples")

        # Duplicate and modify existing samples to reach target
        target_samples = 150000
        current_count = len(self.samples)

        if current_count < target_samples:
            logger.info(f"Expanding dataset from {current_count} to {target_samples} samples")

            # Create modified versions of existing samples
            original_samples = self.samples.copy()
            while len(self.samples) < target_samples:
                for sample in original_samples:
                    if len(self.samples) >= target_samples:
                        break

                    # Create variations
                    modified_sample = CodeSample(
                        instruction=self.modify_instruction(sample.instruction),
                        input=sample.input,
                        output=sample.output,
                        complexity=sample.complexity,
                    )
                    self.samples.append(modified_sample)

        logger.info(f"Final dataset size: {len(self.samples)} samples")

    def modify_instruction(self, instruction: str) -> str:
        """Create variations of instructions"""
        modifications = [
            lambda x: x.replace("Viết", "Tạo"),
            lambda x: x.replace("Tạo", "Xây dựng"),
            lambda x: x.replace("hàm", "function"),
            lambda x: x.replace("function", "method"),
            lambda x: f"Implement {x.lower()}",
            lambda x: f"Code {x.lower()}",
            lambda x: f"Develop {x.lower()}",
        ]

        import random

        modification = random.choice(modifications)
        try:
            return modification(instruction)
        except:
            return instruction

    def save_dataset(self, output_path: str = "vn_python_dataset.jsonl") -> None:
        """Save dataset to JSONL format"""
        output_file = Path(output_path)

        logger.info(f"Saving dataset to {output_file}")

        with open(output_file, "w", encoding="utf-8") as f:
            for sample in self.samples:
                json_data = {
                    "instruction": sample.instruction,
                    "input": sample.input,
                    "output": sample.output,
                    "language": sample.language,
                    "complexity": sample.complexity,
                }
                f.write(json.dumps(json_data, ensure_ascii=False) + "\n")

        logger.info(f"Dataset saved successfully: {len(self.samples)} samples")

        # Print statistics
        complexities = {}
        for sample in self.samples:
            complexities[sample.complexity] = complexities.get(sample.complexity, 0) + 1

        logger.info("Dataset statistics:")
        for complexity, count in complexities.items():
            logger.info(f"  {complexity}: {count} samples")


def main():
    """Main function"""
    if len(sys.argv) != 2:
        print("Usage: python prepare_vn_dataset.py /path/to/your/project")
        sys.exit(1)

    project_path = sys.argv[1]

    if not os.path.exists(project_path):
        print(f"Error: Project path '{project_path}' does not exist")
        sys.exit(1)

    logger.info("🚀 Vietnamese Python Dataset Generator")
    logger.info("====================================")

    generator = VietnameseDatasetGenerator(project_path)
    generator.scan_project()
    generator.save_dataset()

    logger.info("✅ Dataset preparation completed!")
    logger.info("📁 Output: vn_python_dataset.jsonl")
    logger.info(f"📊 Total samples: {len(generator.samples)}")


if __name__ == "__main__":
    main()
