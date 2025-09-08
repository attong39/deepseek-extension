#!/usr/bin/env python
"""
Script quét và phát hiện file trùng lặp (exact duplicate và similarity).

Sử dụng hash để tìm exact duplicate và similarity để tìm near duplicate.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from difflib import SequenceMatcher
from pathlib import Path
from typing import Any
import Exception
import bool
import checked_pairs
import chunk
import data
import dict
import enumerate
import f
import f1
import f2
import file1
import file2
import file_path
import files
import float
import i
import iter
import len
import list
import open
import pattern
import print
import round
import self
import set
import similarity_threshold
import str
import sum
import tuple


class DuplicateFinder:
    """Tìm file trùng lặp trong repository"""

    def __init__(self, repo_root: Path, exclude_patterns: list[str] | None = None):
        self.repo_root = repo_root
        self.exclude_patterns = exclude_patterns or [
            "*.pyc",
            "*.pyo",
            "__pycache__",
            ".git",
            ".venv",
            "node_modules",
            "_archive",
            "*.egg-info",
            ".pytest_cache",
            ".mypy_cache",
        ]
        self.file_hashes: dict[str, list[Path]] = {}
        self.results: dict[str, Any] = {"exact_duplicates": {}, "similar_files": {}, "summary": {}}

    def should_exclude(self, file_path: Path) -> bool:
        """Kiểm tra file có nên loại trừ không"""
        for pattern in self.exclude_patterns:
            if pattern.replace("*", "") in str(file_path):
                return True
        return False

    def calculate_file_hash(self, file_path: Path) -> str:
        """Tính hash của file"""
        try:
            hasher = hashlib.md5()
            with open(file_path, "rb") as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    hasher.update(chunk)
            return hasher.hexdigest()
        except Exception:
            return ""

    def scan_files(self) -> None:
        """Scan tất cả file trong repo"""
        print("🔍 Scanning files...")

        for file_path in self.repo_root.rglob("*"):
            if file_path.is_file() and not self.should_exclude(file_path):
                file_hash = self.calculate_file_hash(file_path)
                if file_hash:
                    if file_hash not in self.file_hashes:
                        self.file_hashes[file_hash] = []
                    self.file_hashes[file_hash].append(file_path)

    def find_exact_duplicates(self) -> None:
        """Tìm file trùng lặp hoàn toàn"""
        print("📋 Finding exact duplicates...")

        for file_hash, files in self.file_hashes.items():
            if len(files) > 1:
                rel_paths = [str(f.relative_to(self.repo_root)) for f in files]
                self.results["exact_duplicates"][file_hash] = {
                    "files": rel_paths,
                    "size": files[0].stat().st_size,
                    "count": len(files),
                }

    def calculate_similarity(self, file1: Path, file2: Path) -> float:
        """Tính độ tương đồng giữa 2 file text"""
        try:
            with open(file1, encoding="utf-8") as f1:
                content1 = f1.read()
            with open(file2, encoding="utf-8") as f2:
                content2 = f2.read()

            return SequenceMatcher(None, content1, content2).ratio()
        except Exception:
            return 0.0

    def find_similar_files(self, similarity_threshold: float = 0.8) -> None:
        """Tìm file có nội dung tương tự (chỉ file .py)"""
        print("🔗 Finding similar files...")

        py_files = [f for f in self.repo_root.rglob("*.py") if f.is_file() and not self.should_exclude(f)]

        checked_pairs: set[tuple[str, str]] = set()

        for i, file1 in enumerate(py_files):
            for file2 in py_files[i + 1 :]:
                file1_str = str(file1)
                file2_str = str(file2)
                pair = (file1_str, file2_str) if file1_str < file2_str else (file2_str, file1_str)
                if pair in checked_pairs:
                    continue
                checked_pairs.add(pair)

                # Skip nếu đã là exact duplicate
                hash1 = self.calculate_file_hash(file1)
                hash2 = self.calculate_file_hash(file2)
                if hash1 == hash2:
                    continue

                similarity = self.calculate_similarity(file1, file2)
                if similarity >= similarity_threshold:
                    rel1 = str(file1.relative_to(self.repo_root))
                    rel2 = str(file2.relative_to(self.repo_root))

                    pair_key = f"{rel1} <-> {rel2}"
                    self.results["similar_files"][pair_key] = {
                        "file1": rel1,
                        "file2": rel2,
                        "similarity": round(similarity, 3),
                        "size1": file1.stat().st_size,
                        "size2": file2.stat().st_size,
                    }

    def generate_summary(self) -> None:
        """Tạo summary report"""
        exact_count = len(self.results["exact_duplicates"])
        similar_count = len(self.results["similar_files"])

        total_exact_files = sum(data["count"] for data in self.results["exact_duplicates"].values())
        total_wasted_space = sum(
            data["size"] * (data["count"] - 1) for data in self.results["exact_duplicates"].values()
        )

        self.results["summary"] = {
            "exact_duplicate_groups": exact_count,
            "total_exact_files": total_exact_files,
            "similar_file_pairs": similar_count,
            "wasted_space_bytes": total_wasted_space,
            "wasted_space_mb": round(total_wasted_space / (1024 * 1024), 2),
        }

    def print_results(self) -> None:
        """In kết quả ra console"""
        print("\n" + "=" * 60)
        print("📊 DUPLICATE DETECTION RESULTS")
        print("=" * 60)

        # Summary
        summary = self.results["summary"]
        print(f"🔍 Exact duplicate groups: {summary['exact_duplicate_groups']}")
        print(f"📁 Total duplicate files: {summary['total_exact_files']}")
        print(f"🔗 Similar file pairs: {summary['similar_file_pairs']}")
        print(f"💾 Wasted space: {summary['wasted_space_mb']} MB")
        print()

        # Exact duplicates
        if self.results["exact_duplicates"]:
            print("🎯 EXACT DUPLICATES:")
            print("-" * 40)
            for file_hash, data in self.results["exact_duplicates"].items():
                print(f"Hash: {file_hash[:8]}... ({data['count']} files, {data['size']} bytes)")
                for file_path in data["files"]:
                    print(f"  📄 {file_path}")
                print()

        # Similar files
        if self.results["similar_files"]:
            print("🔗 SIMILAR FILES:")
            print("-" * 40)
            for data in self.results["similar_files"].values():
                print(f"Similarity: {data['similarity'] * 100:.1f}%")
                print(f"  📄 {data['file1']} ({data['size1']} bytes)")
                print(f"  📄 {data['file2']} ({data['size2']} bytes)")
                print()

    def save_results(self, output_file: Path) -> None:
        """Lưu kết quả vào file JSON"""
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(self.results, f, indent=2, ensure_ascii=False)
        print(f"💾 Results saved to: {output_file}")

    def run_scan(self, similarity_threshold: float = 0.8, output_file: Path | None = None) -> None:
        """Chạy toàn bộ quá trình scan"""
        self.scan_files()
        self.find_exact_duplicates()
        self.find_similar_files(similarity_threshold)
        self.generate_summary()
        self.print_results()

        if output_file:
            self.save_results(output_file)


def main() -> None:
    parser = argparse.ArgumentParser(description="Find duplicate files")
    parser.add_argument(
        "--similarity",
        type=float,
        default=0.8,
        help="Similarity threshold for near duplicates (0.0-1.0)",
    )
    parser.add_argument("--output", type=str, help="Output JSON file path")
    parser.add_argument("--exclude", nargs="*", help="Additional exclude patterns")
    args = parser.parse_args()

    repo_root = Path(__file__).parent.parent.parent

    exclude_patterns = None
    if args.exclude:
        exclude_patterns = [
            "*.pyc",
            "*.pyo",
            "__pycache__",
            ".git",
            ".venv",
            "node_modules",
            "_archive",
            "*.egg-info",
            ".pytest_cache",
            ".mypy_cache",
        ] + args.exclude

    finder = DuplicateFinder(repo_root, exclude_patterns)

    output_file = None
    if args.output:
        output_file = Path(args.output)
    else:
        output_file = repo_root / "duplicate_analysis.json"

    finder.run_scan(args.similarity, output_file)


if __name__ == "__main__":
    main()
