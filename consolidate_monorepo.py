"""
Script để hợp nhất cấu trúc monorepo Zeta
Di chuyển zeta-ai-agent, desktop, backend vào apps/
"""
import argparse
import json
import os
import shutil
import sys
from pathlib import Path
from typing import Any, TypedDict
import Exception
import OSError
import ValueError
import action
import bool
import bytes_
import copied_bytes
import copied_files
import d
import dict
import dir_path
import dirs
import dst
import dst_bytes
import dst_files
import e
import exclude_set
import f
import filenames
import files
import fname
import input
import int
import item
import list
import note
import open
import package_json
import path
import print
import root
import script_dir
import self
import set
import sorted
import src
import src_bytes
import src_files
import str
import tsconfig
import tuple


class Action(TypedDict, total=False):
    action: str
    src: str | None
    dst: str | None
    note: str | None

class Manifest:
    """Collects planned and executed actions for audit and dry-run."""

    def __init__(self: Any) -> Any:
        self.actions: list[Action] = []

    def add(self: Any, action: str, src: str | None=None, dst: str | None=None, note: str | None=None) -> Any:
        self.actions.append(Action(action=action, src=src, dst=dst, note=note))

    def write(self: Any, path: str) -> Any:
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        with open(path, 'w', encoding='utf-8') as f:
            json.dump({'actions': self.actions}, f, indent=2, ensure_ascii=False)

class PackageJson(TypedDict, total=False):
    name: str
    version: str
    description: str
    main: str
    types: str
    scripts: dict[str, str]

class TsConfig(TypedDict, total=False):
    compilerOptions: dict[str, Any]
    include: list[str]
    exclude: list[str]

def create_directories(dry_run: bool, manifest: Manifest) -> Any:
    """Tạo cấu trúc thư mục mới"""
    dirs_to_create = ['apps', 'packages/shared', 'packages/ui-components', 'packages/core-utils', 'tools', 'docs', 'config', 'scripts']
    for dir_path in dirs_to_create:
        if dry_run:
            print(f'[DRY RUN] Sẽ tạo thư mục: {dir_path}')
            manifest.add('mkdir', dst=dir_path)
        else:
            Path(dir_path).mkdir(parents=True, exist_ok=True)
            manifest.add('mkdir', dst=dir_path)
            print(f'✓ Tạo thư mục: {dir_path}')

def _confirm_or_force_remove(dst: str, dry_run: bool, force: bool, manifest: Manifest) -> bool:
    if force:
        if dry_run:
            print(f'[DRY RUN] Sẽ xóa: {dst}')
        else:
            shutil.rmtree(dst)
        manifest.add('rmtree', src=dst)
        return True
    response = input(f'Xóa {dst} và tiếp tục? (y/N): ')
    if response.lower() == 'y':
        if dry_run:
            print(f'[DRY RUN] Sẽ xóa: {dst}')
        else:
            shutil.rmtree(dst)
        manifest.add('rmtree', src=dst)
        return True
    return False

def _log_move(src: str, dst: str, dry_run: bool, manifest: Manifest) -> Any:
    if dry_run:
        print(f'[DRY RUN] Sẽ di chuyển: {src} → {dst}')
    else:
        print(f'📁 Di chuyển: {src} → {dst}')
        shutil.move(src, dst)
    manifest.add('move', src=src, dst=dst)
DEFAULT_EXCLUDES = {'node_modules', 'dist', 'out', '.venv', '.git', '__pycache__', '.ruff_cache', '.mypy_cache', '.pytest_cache', '.vscode'}

def _scan_counts(path: str, excludes: set[str]) -> tuple[int, int]:
    """Scan file count and total bytes, skipping excluded dir names."""
    total_files = 0
    total_bytes = 0
    for root, dirs, filenames in os.walk(path):
        dirs[:] = [d for d in dirs if d not in excludes]
        for fname in filenames:
            fpath = os.path.join(root, fname)
            try:
                total_files += 1
                total_bytes += os.path.getsize(fpath)
            except OSError:
                continue
    return (total_files, total_bytes)

def _copy_tree_filtered(src: str, dst: str, excludes: set[str], dry_run: bool, manifest: Manifest) -> tuple[int, int]:
    """Copy src to dst skipping excluded dir names. Returns (files_copied, bytes_copied)."""
    files_copied = 0
    bytes_copied = 0
    dst_dir = dst
    filenames: list[str] = []
    if dry_run:
        print(f"[DRY RUN] Sẽ sao chép (lọc): {src} → {dst} (bỏ qua: {', '.join(sorted(excludes))})")
        manifest.add('copytree', src=src, dst=dst, note=f'excludes={sorted(excludes)}')
        files, bytes_ = _scan_counts(src, excludes)
        print(f'[DRY RUN] Ước tính: {files} files, {bytes_} bytes')
        return (0, 0)
    for root, dirs, filenames in os.walk(src):
        rel = os.path.relpath(root, src)
        if rel == '.':
            rel = ''
        dirs[:] = [d for d in dirs if d not in excludes]
        dst_dir = os.path.join(dst, rel) if rel else dst
        os.makedirs(dst_dir, exist_ok=True)
        for fname in filenames:
            src_file = os.path.join(root, fname)
            dst_file = os.path.join(dst_dir, fname)
            try:
                shutil.copy2(src_file, dst_file)
                files_copied += 1
                try:
                    bytes_copied += os.path.getsize(src_file)
                except OSError:
                    pass
            except Exception as e:
                print(f'[WARN] Không thể sao chép {src_file} → {dst_file}: {e}')
    manifest.add('copytree', src=src, dst=dst, note=f'excludes={sorted(excludes)}')
    return (files_copied, bytes_copied)

def _process_single_move(src: str, dst: str, *, dry_run: bool, force: bool, manifest: Manifest, mode: str, exclude_set: set[str]) -> None:
    if not os.path.exists(src):
        print(f'⚠️  Thư mục nguồn không tồn tại: {src}')
        return
    if os.path.exists(dst):
        print(f'⚠️  Thư mục đích đã tồn tại: {dst}')
        if not _confirm_or_force_remove(dst, dry_run, force, manifest):
            print(f'⏭️  Bỏ qua: {src}')
            return
    if mode == 'move':
        _log_move(src, dst, dry_run, manifest)
        return
    if not dry_run:
        Path(dst).mkdir(parents=True, exist_ok=True)
    print(f'📄 Bắt đầu copy-swap: {src} → {dst}')
    combined_excludes = DEFAULT_EXCLUDES | exclude_set
    src_files, src_bytes = _scan_counts(src, combined_excludes)
    if dry_run:
        print(f'[DRY RUN] Nguồn (lọc): {src_files} files, {src_bytes} bytes')
    copied_files, copied_bytes = _copy_tree_filtered(src, dst, combined_excludes, dry_run, manifest)
    if dry_run:
        return
    dst_files, dst_bytes = _scan_counts(dst, combined_excludes)
    ok = dst_files == src_files and dst_bytes == src_bytes
    manifest.add('verify', src=src, dst=dst, note=f'src_files={src_files},dst_files={dst_files},src_bytes={src_bytes},dst_bytes={dst_bytes}')
    if not ok:
        print(f'❌ Xác minh thất bại cho {src} → {dst}: src({src_files},{src_bytes}) != dst({dst_files},{dst_bytes})')
        return
    if _confirm_or_force_remove(src, dry_run, True, manifest):
        print(f'✓ Copy-swap hoàn tất: {src} → {dst} ({copied_files} files, {copied_bytes} bytes)')

def move_directories(dry_run: bool, force: bool, manifest: Manifest, mode: str='move', excludes: list[str] | None=None) -> Any:
    """Di chuyển các thư mục chính vào apps/"""
    moves = [('zeta-ai-agent', 'apps/zeta-ai-agent'), ('desktop', 'apps/desktop'), ('backend', 'apps/backend')]
    exclude_set: set[str] = set(excludes or [])
    if mode not in {'move', 'copy-swap'}:
        raise ValueError("mode must be 'move' or 'copy-swap'")
    for src, dst in moves:
        _process_single_move(src, dst, dry_run=dry_run, force=force, manifest=manifest, mode=mode, exclude_set=exclude_set)

def move_scripts(dry_run: bool, manifest: Manifest) -> Any:
    """Di chuyển scripts từ các apps vào scripts/ chung"""
    script_dirs = ['apps/zeta-ai-agent/scripts', 'apps/desktop/scripts']
    for script_dir in script_dirs:
        if os.path.exists(script_dir):
            print(f'📋 Di chuyển scripts từ: {script_dir}')
            for item in os.listdir(script_dir):
                src_path = os.path.join(script_dir, item)
                dst_path = os.path.join('scripts', f'{Path(script_dir).parent.name}_{item}')
                if os.path.exists(dst_path):
                    print(f'⚠️  File đã tồn tại: {dst_path}, bỏ qua')
                    continue
                if dry_run:
                    print(f'  [DRY RUN] Sẽ di chuyển: {src_path} → {dst_path}')
                else:
                    shutil.move(src_path, dst_path)
                    print(f'  → {dst_path}')
                manifest.add('move', src=src_path, dst=dst_path)

def update_package_json(dry_run: bool, manifest: Manifest) -> Any:
    """Cập nhật package.json gốc để hỗ trợ workspaces"""
    package_json_path = 'package.json'
    if not os.path.exists(package_json_path):
        print('⚠️  Không tìm thấy package.json gốc')
        return
    import json
    with open(package_json_path, encoding='utf-8') as f:
        try:
            package_data = json.load(f)
        except json.JSONDecodeError:
            print('⚠️  package.json không hợp lệ')
            return
    if 'workspaces' not in package_data:
        package_data['workspaces'] = ['apps/*', 'packages/*']
        print('✓ Thêm workspaces vào package.json')
        if dry_run:
            print('[DRY RUN] Sẽ ghi package.json cập nhật workspaces')
        else:
            with open(package_json_path, 'w', encoding='utf-8') as f:
                json.dump(package_data, f, indent=2, ensure_ascii=False)
        manifest.add('update', src=package_json_path, note='add workspaces')

def create_shared_package(dry_run: bool, manifest: Manifest) -> Any:
    """Tạo package shared cơ bản"""
    shared_dir = Path('packages/shared')
    shared_dir.mkdir(exist_ok=True)
    package_json: PackageJson = {'name': '@zeta/shared', 'version': '1.0.0', 'description': 'Shared utilities for Zeta monorepo', 'main': 'index.js', 'types': 'index.d.ts', 'scripts': {'build': 'tsc', 'test': 'jest'}}
    pkg_path = shared_dir / 'package.json'
    if dry_run:
        print(f'[DRY RUN] Sẽ tạo: {pkg_path}')
    else:
        with open(pkg_path, 'w', encoding='utf-8') as f:
            json.dump(package_json, f, indent=2, ensure_ascii=False)
    manifest.add('write', dst=str(pkg_path))
    tsconfig: TsConfig = {'compilerOptions': {'target': 'ES2020', 'module': 'commonjs', 'declaration': True, 'outDir': './dist', 'rootDir': './src', 'strict': True, 'esModuleInterop': True}, 'include': ['src/**/*'], 'exclude': ['node_modules', 'dist']}
    ts_path = shared_dir / 'tsconfig.json'
    if dry_run:
        print(f'[DRY RUN] Sẽ tạo: {ts_path}')
    else:
        with open(ts_path, 'w', encoding='utf-8') as f:
            json.dump(tsconfig, f, indent=2, ensure_ascii=False)
    manifest.add('write', dst=str(ts_path))
    if dry_run:
        print(f"[DRY RUN] Sẽ tạo thư mục: {shared_dir / 'src'}")
    else:
        (shared_dir / 'src').mkdir(exist_ok=True)
    manifest.add('mkdir', dst=str(shared_dir / 'src'))
    index_content = "// Shared utilities for Zeta monorepo\n\nexport const VERSION = '1.0.0';\n\nexport function logInfo(message: string) {\n    console.log(`[INFO] ${message}`);\n}\n\nexport function logError(message: string) {\n    console.error(`[ERROR] ${message}`);\n}\n"
    index_path = shared_dir / 'src/index.ts'
    if dry_run:
        print(f'[DRY RUN] Sẽ tạo: {index_path}')
    else:
        with open(index_path, 'w', encoding='utf-8') as f:
            f.write(index_content)
    manifest.add('write', dst=str(index_path))
    print('✓ Tạo package shared')

def main() -> Any:
    parser = argparse.ArgumentParser(description='Consolidate Zeta monorepo')
    parser.add_argument('--dry-run', action='store_true', help='Chỉ in kế hoạch, không thay đổi')
    parser.add_argument('--force', action='store_true', help='Ghi đè thư mục đích nếu tồn tại')
    parser.add_argument('--report', default='consolidation_plan.json', help='Đường dẫn lưu manifest kế hoạch')
    parser.add_argument('--mode', choices=['move', 'copy-swap'], default='move', help="Cách di chuyển: 'move' (mặc định) hoặc 'copy-swap' (sao chép rồi xóa nguồn)")
    parser.add_argument('--exclude', action='append', default=[], help='Tên thư mục cần loại trừ khi copy-swap (repeatable)')
    args = parser.parse_args()
    dry_run = args.dry_run
    force = args.force
    report = args.report
    mode = args.mode
    excludes = list(args.exclude or [])
    print('🚀 Bắt đầu hợp nhất cấu trúc monorepo Zeta')
    print('=' * 50)
    manifest = Manifest()
    try:
        create_directories(dry_run, manifest)
        print()
        move_directories(dry_run, force, manifest, mode=mode, excludes=excludes)
        print()
        move_scripts(dry_run, manifest)
        print()
        update_package_json(dry_run, manifest)
        print()
        create_shared_package(dry_run, manifest)
        print()
        manifest.write(report)
        if dry_run:
            print('✅ Dry run hoàn thành! Không có thay đổi nào được áp dụng.')
            print(f'📄 Manifest kế hoạch: {report}')
        else:
            print('✅ Hoàn thành hợp nhất cấu trúc!')
            print(f'📄 Manifest thao tác: {report}')
        print('\n📋 Các bước tiếp theo:')
        print('1. Kiểm tra các apps hoạt động: npm run build trong apps/*')
        print('2. Cập nhật import paths nếu cần')
        print('3. Test integration giữa các apps')
        print('4. Cập nhật documentation')
    except Exception as e:
        print(f'❌ Lỗi: {e}')
        sys.exit(1)
if __name__ == '__main__':
    main()
