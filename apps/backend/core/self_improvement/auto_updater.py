from __future__ import annotations
import Exception
import FileNotFoundError
import TimeoutError
import ValueError
import bool
import ch
import changes
import cmd
import content
import dict
import diffs
import dst
import e
import e2
import env
import float
import gates
import int
import list
import message
import patch
import path
import qg
import repo
import root
import runner
import self
import snapshot
import src
import staticmethod
import stderr_b
import stdout_b
import str
import timeout_s

"""Core auto‑update engine (v1) — áp dụng patch an toàn + quality gates.

Đặc điểm:
- Patch gồm nhiều thay đổi file (ADD/UPDATE/DELETE/RENAME/MOVE)
- Backup & rollback tự động nếu quality gates fail (ruff/mypy/pytest/...)
- Không phụ thuộc Git, nhưng nếu có git sẽ tự `git add/commit` (best‑effort)
- CLI/runner bất đồng bộ, timeout per‑command
- Diff preview tiện cho UI/PR

Không side‑effect khi import. I/O chỉ xảy ra trong `apply_patch()`.
"""

import asyncio
import difflib
import os
import shutil
import subprocess
import textwrap
import time
import uuid
from collections.abc import Mapping, Sequence
from datetime import UTC, datetime
from enum import Enum
from pathlib import Path
from typing import Protocol

# Pydantic v2
from pydantic import BaseModel, ConfigDict, Field


# --------------------------
# Models
# --------------------------
class OperationType(str, Enum):
    ADD = "ADD"
    UPDATE = "UPDATE"
    DELETE = "DELETE"
    RENAME = "RENAME"
    MOVE = "MOVE"


class FileChange(BaseModel):
    """Một thay đổi trên 1 file.

    Attributes:
        op: loại thao tác.
        path: đường dẫn cũ/đích đối với ADD/UPDATE/DELETE; với RENAME/MOVE là nguồn.
        new_path: đường dẫn mới cho RENAME/MOVE.
        content: nội dung text cho ADD/UPDATE (UTF‑8). None với DELETE/RENAME/MOVE.
    """

    model_config = ConfigDict(extra="forbid")

    op: OperationType
    path: str
    new_path: str | None = None
    content: str | None = None


class Patch(BaseModel):
    """Tập hợp thay đổi cần áp dụng cùng nhau."""

    model_config = ConfigDict(extra="forbid")

    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    title: str
    summary: str | None = None
    changes: list[FileChange] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    dry_run: bool = False


class QualityGateSpec(BaseModel):
    """Định nghĩa chất lượng bắt buộc trước khi giữ patch."""

    model_config = ConfigDict(extra="forbid")

    commands: list[str] = Field(
        default_factory=lambda: [
            "uv run ruff check .",
            "uv run mypy . --strict",
            "uv run pytest -q",
            "uv run pip-audit || true",
            "uv run bandit -r zeta_vn -q || true",
        ]
    )
    timeout_s: float = 900.0
    env: dict[str, str] = Field(default_factory=dict)


class GateRun(BaseModel):
    cmd: str
    exit_code: int
    duration_s: float
    stdout: str = ""
    stderr: str = ""


class PatchResult(BaseModel):
    patch_id: str
    applied: bool
    passed_quality_gates: bool
    rolled_back: bool
    gates: list[GateRun]
    errors: list[str] = Field(default_factory=list)
    commit_hash: str | None = None


# --------------------------
# Repo/Runner protocols
# --------------------------
class RepoAdapter(Protocol):
    root: Path

    def read_text(self, path: str) -> str | None: ...
    def write_text(self, path: str, content: str) -> None: ...
    def delete(self, path: str) -> None: ...
    def move(self, src: str, dst: str) -> None: ...
    def exists(self, path: str) -> bool: ...
    def commit(self, message: str) -> str | None: ...  # returns commit hash if possible


class CommandRunner(Protocol):
    async def run(
        self, cmd: str, *, timeout_s: float, env: Mapping[str, str] | None = None
    ) -> GateRun: ...


# --------------------------
# Implementations
# --------------------------
class LocalFSRepoAdapter:
    """Repo adapter chạy trên filesystem hiện tại. Git commit nếu có git."""

    def __init__(self, root: str | Path) -> None:
        self.root = Path(root).resolve()

    def _abspath(self, path: str) -> Path:
        p = (self.root / path).resolve()
        if not str(p).startswith(str(self.root)):
            raise ValueError("path escapes repository root")
        return p

    def read_text(self, path: str) -> str | None:
        p = self._abspath(path)
        if not p.exists():
            return None
        return p.read_text(encoding="utf-8")

    def write_text(self, path: str, content: str) -> None:
        p = self._abspath(path)
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(content, encoding="utf-8")

    def delete(self, path: str) -> None:
        p = self._abspath(path)
        if p.exists():
            p.unlink()

    def move(self, src: str, dst: str) -> None:
        s = self._abspath(src)
        d = self._abspath(dst)
        d.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(s), str(d))

    def exists(self, path: str) -> bool:
        return self._abspath(path).exists()

    def commit(self, message: str) -> str | None:
        try:
            # Best‑effort commit. Không raise nếu git không có.
            subprocess.run(
                ["git", "add", "-A"],
                cwd=self.root,
                check=False,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
            c = subprocess.run(
                ["git", "commit", "-m", message],
                cwd=self.root,
                check=False,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
            if c.returncode != 0:
                return None
            h = subprocess.run(
                ["git", "rev-parse", "HEAD"],
                cwd=self.root,
                check=False,
                stdout=subprocess.PIPE,
            )
            out = h.stdout.decode().strip()
            return out or None
        except Exception:
            return None


class AsyncShellRunner:
    """Chạy lệnh shell bất đồng bộ với timeout."""

    async def run(
        self, cmd: str, *, timeout_s: float, env: Mapping[str, str] | None = None
    ) -> GateRun:
        start = time.perf_counter()
        try:
            # For Windows compatibility, use shell=False and proper encoding
            p = await asyncio.create_subprocess_shell(
                cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                env=dict(os.environ, **(env or {})),
                shell=False,
            )
            try:
                stdout_b, stderr_b = await asyncio.wait_for(
                    p.communicate(), timeout=timeout_s
                )
                rc = p.returncode or 0
                stdout = stdout_b.decode("utf-8", errors="replace") if stdout_b else ""
                stderr = stderr_b.decode("utf-8", errors="replace") if stderr_b else ""
            except TimeoutError:
                try:
                    p.kill()
                    await p.wait()
                except Exception:
                    pass
                return GateRun(
                    cmd=cmd,
                    exit_code=124,
                    duration_s=time.perf_counter() - start,
                    stdout="",
                    stderr="TIMEOUT",
                )
        except Exception as e:
            return GateRun(
                cmd=cmd,
                exit_code=1,
                duration_s=time.perf_counter() - start,
                stdout="",
                stderr=str(e),
            )
        return GateRun(
            cmd=cmd,
            exit_code=rc,
            duration_s=time.perf_counter() - start,
            stdout=stdout,
            stderr=stderr,
        )


# --------------------------
# AutoUpdater (v1)
# --------------------------
class AutoUpdater:
    """Áp dụng patch với rollback + quality gates.

    Example:
        repo = LocalFSRepoAdapter(".")
        runner = AsyncShellRunner()
        updater = AutoUpdater(repo, runner)
        res = await updater.apply_patch(patch, QualityGateSpec())
    """

    def __init__(self, repo: RepoAdapter, runner: CommandRunner) -> None:
        self.repo = repo
        self.runner = runner

    # ---------- preview ----------
    def preview(self, patch: Patch) -> dict[str, str]:
        """Tạo unified diff cho từng file để hiển thị trước khi áp dụng."""
        diffs: dict[str, str] = {}
        for ch in patch.changes:
            old = (
                self.repo.read_text(ch.path)
                if ch.op
                in {
                    OperationType.UPDATE,
                    OperationType.DELETE,
                    OperationType.RENAME,
                    OperationType.MOVE,
                }
                else ""
            )
            new_path = ch.new_path or ch.path
            if ch.op == OperationType.DELETE:
                new = ""
            elif ch.op in {OperationType.RENAME, OperationType.MOVE}:
                # rename không đổi nội dung; hiển thị meta diff
                new = old or ""
            else:
                new = ch.content or ""
            diff = difflib.unified_diff(
                (old or "").splitlines(keepends=True),
                (new or "").splitlines(keepends=True),
                fromfile=ch.path,
                tofile=new_path,
            )
            diffs[ch.path] = "".join(diff)
        return diffs

    # ---------- apply ----------
    async def apply_patch(self, patch: Patch, qg: QualityGateSpec) -> PatchResult:
        """Áp dụng patch và chạy quality gates. Tự rollback nếu fail.

        Args:
            patch: patch cần áp dụng.
            qg: bộ lệnh kiểm thử chất lượng.
        """
        # 1) Backup snapshot (để rollback nếu cần)
        snapshot: list[FileChange] = []
        try:
            for ch in patch.changes:
                if ch.op in {OperationType.ADD}:
                    # backup ADD = xoá file mới nếu rollback
                    snapshot.append(FileChange(op=OperationType.DELETE, path=ch.path))
                elif ch.op in {OperationType.UPDATE}:
                    old = self.repo.read_text(ch.path) or ""
                    snapshot.append(
                        FileChange(op=OperationType.UPDATE, path=ch.path, content=old)
                    )
                elif ch.op in {OperationType.DELETE}:
                    old = self.repo.read_text(ch.path) or ""
                    snapshot.append(
                        FileChange(op=OperationType.ADD, path=ch.path, content=old)
                    )
                elif ch.op in {OperationType.RENAME, OperationType.MOVE}:
                    snapshot.append(
                        FileChange(
                            op=OperationType.MOVE,
                            path=ch.new_path or ch.path,
                            new_path=ch.path,
                        )
                    )
        except Exception as e:
            return PatchResult(
                patch_id=patch.id,
                applied=False,
                passed_quality_gates=False,
                rolled_back=False,
                gates=[],
                errors=[f"snapshot error: {e}"],
            )

        # 2) Apply patch (dry‑run skip write)
        try:
            if not patch.dry_run:
                self._apply_changes(patch.changes)
        except Exception as e:
            # apply lỗi => không chạy gates, rollback snapshot apply‑partial
            try:
                if not patch.dry_run:
                    self._apply_changes(snapshot)
            except Exception as e2:
                return PatchResult(
                    patch_id=patch.id,
                    applied=False,
                    passed_quality_gates=False,
                    rolled_back=False,
                    gates=[],
                    errors=[f"apply error: {e}", f"rollback failed: {e2}"],
                )
            return PatchResult(
                patch_id=patch.id,
                applied=False,
                passed_quality_gates=False,
                rolled_back=True,
                gates=[],
                errors=[f"apply error: {e}"],
            )

        # 3) Run quality gates
        gates: list[GateRun] = []
        all_passed = True
        for cmd in qg.commands:
            run = await self.runner.run(cmd, timeout_s=qg.timeout_s, env=qg.env)
            gates.append(run)
            if run.exit_code != 0:
                all_passed = False
                break

        if not all_passed:
            # Rollback
            try:
                if not patch.dry_run:
                    self._apply_changes(snapshot)
            except Exception as e2:
                return PatchResult(
                    patch_id=patch.id,
                    applied=True,
                    passed_quality_gates=False,
                    rolled_back=False,
                    gates=gates,
                    errors=[f"rollback failed: {e2}"],
                )
            return PatchResult(
                patch_id=patch.id,
                applied=True,
                passed_quality_gates=False,
                rolled_back=True,
                gates=gates,
                errors=["quality gates failed"],
            )

        # 4) Commit (best‑effort)
        commit_hash = None
        if not patch.dry_run:
            commit_hash = self.repo.commit(self._build_commit_message(patch))

        return PatchResult(
            patch_id=patch.id,
            applied=True,
            passed_quality_gates=True,
            rolled_back=False,
            gates=gates,
            errors=[],
            commit_hash=commit_hash,
        )

    # ---------- helpers ----------
    def _apply_changes(self, changes: Sequence[FileChange]) -> None:
        for ch in changes:
            if ch.op == OperationType.ADD:
                self.repo.write_text(ch.path, ch.content or "")
            elif ch.op == OperationType.UPDATE:
                if not self.repo.exists(ch.path):
                    raise FileNotFoundError(f"update target not found: {ch.path}")
                self.repo.write_text(ch.path, ch.content or "")
            elif ch.op == OperationType.DELETE:
                self.repo.delete(ch.path)
            elif ch.op in {OperationType.RENAME, OperationType.MOVE}:
                if not ch.new_path:
                    raise ValueError("new_path required for RENAME/MOVE")
                self.repo.move(ch.path, ch.new_path)
            else:
                raise ValueError(f"unsupported op: {ch.op}")

    @staticmethod
    def _build_commit_message(patch: Patch) -> str:
        summary = (patch.summary or "").strip()
        body = (
            textwrap.shorten(summary, width=400, placeholder=" …")
            if summary
            else "Auto‑update"
        )
        return f"chore(auto‑update): {patch.title}\n\n{body}\n\nPatch‑Id: {patch.id}"
