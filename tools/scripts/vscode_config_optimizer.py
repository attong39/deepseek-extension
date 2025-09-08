from __future__ import annotations

import json
import shutil
from datetime import datetime
from pathlib import Path
from typing import Any

from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.table import Table
import Exception
import any
import category
import dict
import e
import f
import feature
import features
import filename
import files
import isinstance
import k
import key
import key1
import key2
import keyword
import len
import list
import open
import progress
import round
import self
import set
import setting
import setting_key
import settings
import settings1
import settings2
import str
import task
import tasks
import v
import value

"""
🔧 VSCode Configuration Optimizer
Tối ưu và hợp nhất các file cấu hình VSCode để loại bỏ trùng lặp và đảm bảo nhất quán.
"""


class VSCodeConfigOptimizer:
    """Tối ưu cấu hình VSCode với phân tích trùng lặp và hợp nhất thông minh."""

    def __init__(self, workspace_root: Path):
        self.workspace_root = workspace_root
        self.vscode_dir = workspace_root / ".vscode"
        self.console = Console()
        self.backup_dir = self.vscode_dir / "backup" / datetime.now().strftime("%Y%m%d_%H%M%S")
        self.config_files = [
            "settings.json",
            "settings_clean.jsonc",
            "settings_copilot_clean.json",
            "settings_copilot_intelligent.jsonc",
            "settings_copilot_optimized.jsonc",
            "settings_copilot_super_intelligent.json",
            "settings_copilot_super_intelligent.jsonc",
            "settings_enhanced.jsonc",
            "settings_minimal.json",
            "settings_self_management.jsonc",
            "tasks.json",
        ]
        self.optimized_templates = {
            "base": {},
            "copilot_basic": {},
            "copilot_advanced": {},
            "copilot_super": {},
            "tasks": {},
        }

    def analyze_configurations(self) -> dict[str, Any]:
        """Phân tích tất cả file cấu hình để tìm trùng lặp và xung đột."""
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=self.console,
        ) as progress:
            progress.add_task("🔍 Analyzing configurations...", total=None)
            analysis = {
                "files_found": [],
                "duplicates": {},
                "conflicts": {},
                "missing_features": {},
                "size_analysis": {},
                "recommendations": [],
            }
            all_settings = {}
            for filename in self.config_files:
                file_path = self.vscode_dir / filename
                if file_path.exists():
                    try:
                        content = self._load_json_file(file_path)
                        if content:
                            all_settings[filename] = content
                            analysis["files_found"].append(filename)
                            analysis["size_analysis"][filename] = {
                                "size_kb": round(file_path.stat().st_size / 1024, 2),
                                "settings_count": len(content) if isinstance(content, dict) else 0,
                                "last_modified": datetime.fromtimestamp(file_path.stat().st_mtime).isoformat(),
                            }
                    except Exception as e:
                        self.console.print(f"❌ Error reading {filename}: {e}")
            analysis["duplicates"] = self._find_duplicates(all_settings)
            analysis["conflicts"] = self._find_conflicts(all_settings)
            analysis["missing_features"] = self._find_missing_features(all_settings)
            analysis["recommendations"] = self._generate_recommendations(analysis)
            return analysis

    def _load_json_file(self, file_path: Path) -> dict[str, Any] | None:
        """Load JSON/JSONC file với xử lý comments."""
        try:
            content = file_path.read_text(encoding="utf-8")
            if file_path.suffix == ".jsonc":
                lines = []
                for line in content.split("\n"):
                    if "//" in line:
                        line = line[: line.index("//")]
                    lines.append(line)
                content = "\n".join(lines)
            return json.loads(content)
        except json.JSONDecodeError as e:
            self.console.print(f"⚠️ JSON parsing error in {file_path.name}: {e}")
            return None
        except Exception as e:
            self.console.print(f"❌ Error loading {file_path.name}: {e}")
            return None

    def _find_duplicates(self, all_settings: dict[str, dict]) -> dict[str, list[str]]:
        """Tìm các setting trùng lặp giữa các file."""
        duplicates = {}
        for key1, settings1 in all_settings.items():
            for key2, settings2 in all_settings.items():
                if key1 >= key2:  # Tránh so sánh trùng lặp
                    continue
                common_keys = set(settings1.keys()) & set(settings2.keys())
                for setting_key in common_keys:
                    if settings1[setting_key] == settings2[setting_key]:
                        dup_key = f"{setting_key}"
                        if dup_key not in duplicates:
                            duplicates[dup_key] = []
                        file_pair = f"{key1} ↔ {key2}"
                        if file_pair not in duplicates[dup_key]:
                            duplicates[dup_key].append(file_pair)
        return duplicates

    def _find_conflicts(self, all_settings: dict[str, dict]) -> dict[str, dict]:
        """Tìm các setting xung đột (cùng key nhưng khác value)."""
        conflicts = {}
        all_keys = set()
        for settings in all_settings.values():
            all_keys.update(settings.keys())
        for key in all_keys:
            values = {}
            for filename, settings in all_settings.items():
                if key in settings:
                    value_str = json.dumps(settings[key], sort_keys=True)
                    if value_str not in values:
                        values[value_str] = []
                    values[value_str].append(filename)
            if len(values) > 1:
                conflicts[key] = values
        return conflicts

    def _find_missing_features(self, all_settings: dict[str, dict]) -> dict[str, list[str]]:
        """Tìm các tính năng quan trọng bị thiếu."""
        essential_features = {
            "copilot_basic": [
                "github.copilot.enable",
                "github.copilot.editor.enableAutoCompletions",
            ],
            "copilot_advanced": [
                "github.copilot.inlineSuggest.enable",
                "github.copilot.chat.followUps",
                "chat.extensionTools.enabled",
            ],
            "python_analysis": [
                "python.analysis.typeCheckingMode",
                "python.languageServer",
                "python.analysis.autoImportCompletions",
            ],
            "code_quality": ["editor.formatOnSave", "editor.codeActionsOnSave", "ruff.enable"],
            "project_structure": [
                "files.associations",
                "explorer.fileNesting.enabled",
                "python.analysis.extraPaths",
            ],
        }
        missing = {}
        for category, features in essential_features.items():
            missing[category] = []
            for filename, settings in all_settings.items():
                if "copilot" in filename.lower() or filename == "settings.json":
                    for feature in features:
                        if feature not in settings:
                            missing[category].append(f"{filename}: missing {feature}")
        missing = {k: v for k, v in missing.items() if v}
        return missing

    def _generate_recommendations(self, analysis: dict[str, Any]) -> list[str]:
        """Tạo khuyến nghị tối ưu dựa trên phân tích."""
        recommendations = []
        if analysis["duplicates"]:
            recommendations.append(
                f"🔄 Found {len(analysis['duplicates'])} duplicate settings. "
                "Consider consolidating into fewer configuration files."
            )
        if analysis["conflicts"]:
            recommendations.append(
                f"⚠️ Found {len(analysis['conflicts'])} conflicting settings. "
                "Review and standardize these configurations."
            )
        file_count = len(analysis["files_found"])
        if file_count > 5:
            recommendations.append(
                f"📁 Too many config files ({file_count}). " "Recommend consolidating to 3-4 purpose-specific files."
            )
        if analysis["missing_features"]:
            recommendations.append(
                "✨ Some important features are missing in certain configs. "
                "Consider adding them for better development experience."
            )
        recommendations.extend(
            [
                "🎯 Recommended structure:",
                "  • settings.json - Main active configuration",
                "  • settings_copilot_optimal.json - Best Copilot setup",
                "  • settings_minimal.json - Lightweight for testing",
                "  • tasks.json - Development tasks",
            ]
        )
        return recommendations

    def create_optimized_configs(self) -> None:
        """Tạo các file cấu hình tối ưu mới."""
        self.console.print("\n🔧 Creating optimized configurations...")
        self._create_backup()
        self._create_base_config()
        self._create_copilot_optimal_config()
        self._create_minimal_config()
        self._optimize_tasks_config()
        self.console.print("✅ Optimized configurations created successfully!")

    def _create_backup(self) -> None:
        """Backup tất cả file cấu hình hiện tại."""
        self.backup_dir.mkdir(parents=True, exist_ok=True)
        for filename in self.config_files:
            file_path = self.vscode_dir / filename
            if file_path.exists():
                backup_path = self.backup_dir / filename
                shutil.copy2(file_path, backup_path)
        self.console.print(f"💾 Backup created: {self.backup_dir}")

    def _create_base_config(self) -> None:
        """Tạo cấu hình cơ bản tối ưu (settings.json)."""
        config = {
            "// ZETA_VN - Optimized Development Configuration": "Generated by VSCode Config Optimizer",
            "python.languageServer": "Pylance",
            "python.defaultInterpreterPath": "${workspaceFolder}/.venv/Scripts/python.exe",
            "python.analysis.typeCheckingMode": "strict",
            "python.analysis.autoSearchPaths": True,
            "python.analysis.autoImportCompletions": True,
            "python.analysis.diagnosticMode": "workspace",
            "python.analysis.completeFunctionParens": True,
            "python.analysis.importFormat": "absolute",
            "python.analysis.include": ["zeta_vn/**", "tests/**", "tools/**"],
            "python.analysis.extraPaths": ["${workspaceFolder}", "${workspaceFolder}/zeta_vn"],
            "python.analysis.exclude": [
                "**/.venv/**",
                "**/__pycache__/**",
                "**/.pytest_cache/**",
                "**/.mypy_cache/**",
            ],
            "editor.formatOnSave": True,
            "editor.codeActionsOnSave": {
                "source.fixAll.ruff": "explicit",
                "source.organizeImports.ruff": "explicit",
            },
            "ruff.enable": True,
            "ruff.lint.enable": True,
            "ruff.format.enable": True,
            "ruff.organizeImports": True,
            "[python]": {
                "editor.defaultFormatter": "charliermarsh.ruff",
                "editor.formatOnSave": True,
                "editor.codeActionsOnSave": {
                    "source.fixAll.ruff": "explicit",
                    "source.organizeImports.ruff": "explicit",
                },
            },
            "files.associations": {
                "*.py": "python",
                "**/zeta_vn/core/domain/**/*.py": "python",
                "**/zeta_vn/core/use_cases/**/*.py": "python",
                "**/zeta_vn/core/services/**/*.py": "python",
                "**/zeta_vn/core/interfaces/**/*.py": "python",
                "**/zeta_vn/app/api/**/*.py": "python",
                "**/zeta_vn/data/**/*.py": "python",
                "**/tests/**/*.py": "python",
                "pyproject.toml": "toml",
                "uv.lock": "toml",
                ".python-version": "plaintext",
                "PROJECT_MAP.md": "markdown",
                "GUIDE.md": "markdown",
                ".copilot-instructions.md": "markdown",
            },
            "explorer.fileNesting.enabled": True,
            "explorer.fileNesting.expand": False,
            "explorer.fileNesting.patterns": {
                "*.py": "${capture}_test.py, test_${capture}.py, ${capture}.pyi",
                "entity.py": "value_objects.py, domain_events.py, exceptions.py",
                "repository.py": "repository_impl.py, repository_mock.py",
                "service.py": "service_impl.py, service_test.py",
                "use_case.py": "use_case_impl.py, use_case_test.py",
                "router.py": "schemas.py, dependencies.py, exceptions.py",
                "main.py": "config.py, dependencies.py, middleware.py",
                "pyproject.toml": "requirements*.txt, uv.lock, .python-version",
                ".env": ".env.example, .env.local, .env.production",
                "README.md": "CHANGELOG.md, LICENSE, CONTRIBUTING.md",
            },
            "files.exclude": {
                "**/__pycache__": True,
                "**/.pytest_cache": True,
                "**/.mypy_cache": True,
                "**/.ruff_cache": True,
                "**/*.pyc": True,
            },
            "search.exclude": {
                "**/.venv/**": True,
                "**/__pycache__/**": True,
                "**/.pytest_cache/**": True,
                "**/.mypy_cache/**": True,
                "**/.ruff_cache/**": True,
                "**/node_modules/**": True,
                "**/.git/**": True,
                "**/dist/**": True,
                "**/build/**": True,
            },
            "python.testing.pytestEnabled": True,
            "python.testing.pytestArgs": ["tests"],
            "python.testing.cwd": "${workspaceFolder}",
            "emeraldwalk.runonsave": {
                "commands": [{"match": "\\.py$", "cmd": 'uv run python .copilot/on_save_fix.py "${file}"'}]
            },
        }
        self._save_config(self.vscode_dir / "settings.json", config)

    def _create_copilot_optimal_config(self) -> None:
        """Tạo cấu hình Copilot tối ưu nhất."""
        config = {
            "// ZETA_VN - Copilot Super Intelligent Configuration": "Maximum AI assistance for ZETA_VN project",
            "github.copilot.enable": {
                "*": True,
                "yaml": True,
                "json": True,
                "jsonc": True,
                "python": True,
                "typescript": True,
                "javascript": True,
                "markdown": True,
                "toml": True,
                "dockerfile": True,
                "shellscript": True,
            },
            "github.copilot.editor.enableAutoCompletions": True,
            "github.copilot.editor.enableCodeActions": True,
            "github.copilot.editor.iterativeEditing": True,
            "github.copilot.inlineSuggest.enable": True,
            "github.copilot.inlineSuggest.count": 3,
            "github.copilot.chat.followUps": "on",
            "github.copilot.chat.localeOverride": "en",
            "github.copilot.chat.welcomeMessage": "never",
            "chat.extensionTools.enabled": True,
            "chat.implicitContext.suggestedContext": True,
            "chat.promptFiles": True,
            "chat.experimental.multiTurn": True,
            "editor.inlineSuggest.enabled": True,
            "editor.inlineSuggest.showToolbar": "always",
            "editor.suggest.preview": True,
            "editor.suggest.showInlineDetails": True,
            "editor.suggest.insertMode": "replace",
            "editor.suggest.showWords": False,
            "editor.acceptSuggestionOnCommitCharacter": True,
            "editor.acceptSuggestionOnEnter": "on",
            **self._get_base_settings(),
            "explorer.fileNesting.patterns": {
                **self._get_base_file_nesting(),
                ".copilot-instructions.md": "copilot-instructions.md, .copilot/**",
                "PROJECT_MAP.md": "update_project_map.py, GUIDE.md, ARCHITECTURE.md",
                "*.py": "${capture}_test.py, test_${capture}.py, ${capture}.pyi, ${capture}_schema.py, ${capture}_types.py",
            },
        }
        self._save_config(self.vscode_dir / "settings_copilot_optimal.json", config)

    def _create_minimal_config(self) -> None:
        """Tạo cấu hình minimal cho testing và performance."""
        config = {
            "// ZETA_VN - Minimal Configuration": "Lightweight setup for testing and performance",
            "python.languageServer": "Pylance",
            "python.defaultInterpreterPath": "${workspaceFolder}/.venv/Scripts/python.exe",
            "python.analysis.typeCheckingMode": "basic",
            "python.analysis.autoImportCompletions": True,
            "editor.formatOnSave": True,
            "ruff.enable": True,
            "[python]": {"editor.defaultFormatter": "charliermarsh.ruff"},
            "files.associations": {"*.py": "python", "pyproject.toml": "toml"},
            "files.exclude": {"**/__pycache__": True, "**/.pytest_cache": True},
            "github.copilot.enable": {"*": False},
            "explorer.fileNesting.enabled": False,
            "python.analysis.diagnosticMode": "openFilesOnly",
        }
        self._save_config(self.vscode_dir / "settings_minimal.json", config)

    def _optimize_tasks_config(self) -> None:
        """Tối ưu file tasks.json để loại bỏ trùng lặp."""
        tasks_file = self.vscode_dir / "tasks.json"
        if not tasks_file.exists():
            return
        try:
            content = self._load_json_file(tasks_file)
            if not content or "tasks" not in content:
                return
            seen_labels = set()
            unique_tasks = []
            for task in content["tasks"]:
                label = task.get("label", "")
                if label and label not in seen_labels:
                    seen_labels.add(label)
                    unique_tasks.append(task)
            categorized_tasks = self._categorize_tasks(unique_tasks)
            optimized_content = {"version": "2.0.0", "tasks": categorized_tasks}
            self._save_config(tasks_file, optimized_content)
        except Exception as e:
            self.console.print(f"❌ Error optimizing tasks.json: {e}")

    def _categorize_tasks(self, tasks: list[dict]) -> list[dict]:
        """Sắp xếp tasks theo category để dễ quản lý."""
        categories = {
            "qa": [],  # Quality Assurance
            "copilot": [],  # Copilot related
            "dev": [],  # Development
            "test": [],  # Testing
            "build": [],  # Build & Deploy
            "other": [],  # Others
        }
        for task in tasks:
            label = task.get("label", "").lower()
            if any(keyword in label for keyword in ["qa", "quality", "ruff", "mypy", "pytest"]):
                categories["qa"].append(task)
            elif "copilot" in label:
                categories["copilot"].append(task)
            elif any(keyword in label for keyword in ["dev", "server", "watch"]):
                categories["dev"].append(task)
            elif "test" in label:
                categories["test"].append(task)
            elif any(keyword in label for keyword in ["build", "deploy", "compile"]):
                categories["build"].append(task)
            else:
                categories["other"].append(task)
        ordered_tasks = []
        for category in ["qa", "copilot", "dev", "test", "build", "other"]:
            ordered_tasks.extend(categories[category])
        return ordered_tasks

    def _get_base_settings(self) -> dict[str, Any]:
        """Lấy base settings để tái sử dụng."""
        return {
            "python.languageServer": "Pylance",
            "python.defaultInterpreterPath": "${workspaceFolder}/.venv/Scripts/python.exe",
            "python.analysis.typeCheckingMode": "strict",
            "python.analysis.autoSearchPaths": True,
            "python.analysis.autoImportCompletions": True,
            "python.analysis.extraPaths": ["${workspaceFolder}", "${workspaceFolder}/zeta_vn"],
            "editor.formatOnSave": True,
            "ruff.enable": True,
            "files.exclude": {
                "**/__pycache__": True,
                "**/.pytest_cache": True,
                "**/.mypy_cache": True,
                "**/.ruff_cache": True,
            },
        }

    def _get_base_file_nesting(self) -> dict[str, str]:
        """Lấy base file nesting patterns."""
        return {
            "*.py": "${capture}_test.py, test_${capture}.py, ${capture}.pyi",
            "entity.py": "value_objects.py, domain_events.py, exceptions.py",
            "repository.py": "repository_impl.py, repository_mock.py",
            "service.py": "service_impl.py, service_test.py",
            "pyproject.toml": "requirements*.txt, uv.lock, .python-version",
        }

    def _save_config(self, file_path: Path, config: dict[str, Any]) -> None:
        """Lưu cấu hình với format đẹp."""
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(config, f, indent=2, ensure_ascii=False)
            self.console.print(f"✅ Created: {file_path.name}")
        except Exception as e:
            self.console.print(f"❌ Error saving {file_path.name}: {e}")

    def cleanup_old_files(self) -> None:
        """Dọn dẹp các file cấu hình cũ/trùng lặp."""
        files_to_remove = [
            "settings_copilot_intelligent.jsonc",
            "settings_copilot_optimized.jsonc",
            "settings_copilot_super_intelligent.json",
            "settings_copilot_super_intelligent.jsonc",
            "settings_enhanced.jsonc",
            "settings_self_management.jsonc",
            "settings_clean.jsonc",  # Giữ lại nếu cần cho tham khảo
        ]
        removed_count = 0
        for filename in files_to_remove:
            file_path = self.vscode_dir / filename
            if file_path.exists():
                try:
                    file_path.unlink()
                    removed_count += 1
                    self.console.print(f"🗑️ Removed: {filename}")
                except Exception as e:
                    self.console.print(f"❌ Error removing {filename}: {e}")
        if removed_count > 0:
            self.console.print(f"✅ Cleaned up {removed_count} duplicate configuration files")

    def display_analysis_report(self, analysis: dict[str, Any]) -> None:
        """Hiển thị báo cáo phân tích với Rich UI."""
        self.console.print("\n")
        self.console.print(Panel.fit("🔍 VSCODE CONFIGURATION ANALYSIS REPORT", style="bold blue"))
        files_table = Table(title="📁 Configuration Files Found")
        files_table.add_column("File", style="cyan")
        files_table.add_column("Size (KB)", justify="right")
        files_table.add_column("Settings Count", justify="right")
        files_table.add_column("Last Modified", style="dim")
        for filename in analysis["files_found"]:
            size_info = analysis["size_analysis"][filename]
            files_table.add_row(
                filename,
                str(size_info["size_kb"]),
                str(size_info["settings_count"]),
                size_info["last_modified"][:16],  # Show date only
            )
        self.console.print(files_table)
        if analysis["duplicates"]:
            dup_table = Table(title="🔄 Duplicate Settings")
            dup_table.add_column("Setting Key", style="yellow")
            dup_table.add_column("Found In Files", style="dim")
            for setting, files in analysis["duplicates"].items():
                dup_table.add_row(setting, ", ".join(files))
            self.console.print(dup_table)
        if analysis["conflicts"]:
            conf_table = Table(title="⚠️ Conflicting Settings")
            conf_table.add_column("Setting Key", style="red")
            conf_table.add_column("Different Values In", style="dim")
            for setting, values in analysis["conflicts"].items():
                files_with_conflicts = []
                for value, files in values.items():
                    files_with_conflicts.append(f"{', '.join(files)} ({value[:50]}...)")
                conf_table.add_row(setting, " | ".join(files_with_conflicts))
            self.console.print(conf_table)
        self.console.print("\n")
        self.console.print(Panel("\n".join(analysis["recommendations"]), title="💡 Recommendations", style="green"))


def main():
    """Main function để chạy optimizer."""
    workspace_root = Path.cwd()
    optimizer = VSCodeConfigOptimizer(workspace_root)
    console = Console()
    console.print(
        Panel.fit(
            "🔧 VSCODE CONFIGURATION OPTIMIZER\n" "Analyzing and optimizing VSCode configurations for ZETA_VN",
            style="bold cyan",
        )
    )
    analysis = optimizer.analyze_configurations()
    optimizer.display_analysis_report(analysis)
    console.print("\n")
    create_optimized = console.input("🤖 Create optimized configurations? [y/N]: ").lower().strip()
    if create_optimized == "y":
        optimizer.create_optimized_configs()
        cleanup = console.input("🧹 Clean up old duplicate files? [y/N]: ").lower().strip()
        if cleanup == "y":
            optimizer.cleanup_old_files()
    console.print("\n✨ VSCode Configuration Optimization Complete!")


if __name__ == "__main__":
    main()
