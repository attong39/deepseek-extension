#!/usr/bin/env python3
"""
DeepSeek R1 Agent Terminal Runner

Script để chạy DeepSeek R1 agent trực tiếp từ terminal mà không cần VS Code.
Hỗ trợ Windows, Linux, macOS.

Usage:
    python run_deepseek_agent.py [command] [options]

Commands:
    chat        - Chat với AI agent
    review      - Review code file
    optimize    - Optimize code
    test        - Generate tests
    setup       - Kiểm tra setup
    help        - Hiển thị help

Examples:
    python run_deepseek_agent.py chat "Hello, how are you?"
    python run_deepseek_agent.py review src/extension.ts
    python run_deepseek_agent.py optimize src/aiAgent.ts
    python run_deepseek_agent.py test --file src/extension.ts
    python run_deepseek_agent.py setup --verbose
"""

import argparse
import asyncio
import json
import logging
import os
import subprocess
import sys
import time
from pathlib import Path
from typing import Any, Dict, List, Optional

# Import ollama
try:
    import ollama
except ImportError:
    print("❌ Cần cài đặt ollama package: pip install ollama")
    print("💡 Chạy: pip install ollama")
    sys.exit(1)

# Import httpx cho connection check
try:
    import httpx
except ImportError:
    print("❌ Cần cài đặt httpx package: pip install httpx")
    print("💡 Chạy: pip install httpx")
    sys.exit(1)

# Constants
ERROR_FILE_NOT_FOUND = "❌ File không tồn tại: {}"
ERROR_MISSING_FILE_ARG = "❌ Cần cung cấp file path với --file hoặc -f"
ERROR_MISSING_MESSAGE_ARG = "❌ Cần cung cấp message với --message hoặc -m"
ERROR_PERMISSION_DENIED = "❌ Không có quyền truy cập file: {}"
ERROR_INVALID_PATH = "❌ Đường dẫn không hợp lệ hoặc nằm ngoài project: {}"
ERROR_CONNECTION_FAILED = "❌ Không thể kết nối Ollama server"
ERROR_MODEL_NOT_FOUND = "❌ Model không tìm thấy: {}"

# Security: Chỉ cho phép truy cập trong thư mục project
ALLOWED_BASE_DIRS = [
    os.getcwd(),  # Thư mục hiện tại
    str(Path(__file__).parent),  # Thư mục chứa script
    str(Path(__file__).parent.parent),  # Thư mục cha
]


class DeepSeekAgent:
    """DeepSeek R1 Agent cho terminal operations."""

    def __init__(
        self,
        model: str = "gpt-oss:20b",  # Thay đổi model mặc định
        base_url: str = "http://127.0.0.1:11434",
        verbose: bool = False,
    ):
        self.model = model
        self.base_url = base_url
        self.verbose = verbose
        self.client = ollama.Client(host=base_url)

        # Setup logging
        self.logger = logging.getLogger(__name__)
        if verbose:
            logging.basicConfig(level=logging.DEBUG)
        else:
            logging.basicConfig(level=logging.INFO)

    def validate_file_path(self, file_path: str) -> bool:
        """Kiểm tra tính hợp lệ và bảo mật của đường dẫn file."""
        try:
            # Chuyển thành absolute path
            abs_path = Path(file_path).resolve()

            # Kiểm tra xem file có nằm trong các thư mục cho phép không
            allowed = False
            for base_dir in ALLOWED_BASE_DIRS:
                base_path = Path(base_dir).resolve()
                try:
                    abs_path.relative_to(base_path)
                    allowed = True
                    break
                except ValueError:
                    continue

            if not allowed:
                print(ERROR_INVALID_PATH.format(file_path))
                return False

            # Kiểm tra quyền truy cập
            if not os.access(abs_path, os.R_OK):
                print(ERROR_PERMISSION_DENIED.format(file_path))
                return False

            return True

        except Exception as e:
            print(f"❌ Lỗi validate path: {e}")
            return False

    def check_ollama_connection(self) -> bool:
        """Kiểm tra kết nối Ollama."""
        try:
            # Test connection bằng cách list models với timeout
            with httpx.Client(timeout=10.0) as client:
                response = client.get(f"{self.base_url}/api/tags")
                if response.status_code == 200:
                    return True
                else:
                    print(f"❌ HTTP {response.status_code} từ Ollama server")
                    return False
        except httpx.TimeoutException:
            print("❌ Timeout kết nối Ollama (10s)")
            print("💡 Đảm bảo Ollama đang chạy: ollama serve")
            return False
        except Exception as e:
            print(f"❌ Không thể kết nối Ollama: {e}")
            print("💡 Đảm bảo Ollama đang chạy: ollama serve")
            return False

    def chat(self, message: str, context: Optional[List[Dict[str, Any]]] = None) -> str:
        """Chat với DeepSeek R1."""
        messages = context or []
        messages.append({"role": "user", "content": message})

        try:
            self.logger.debug(f"Gửi message: {message[:100]}...")
            # Thêm timeout cho Ollama call
            import time

            start_time = time.time()

            response = self.client.chat(
                model=self.model,
                messages=messages,
                stream=False,
                options={"timeout": 120},  # Tăng timeout lên 120 giây
            )

            elapsed = time.time() - start_time
            self.logger.debug(
                f"Nhận response sau {elapsed:.2f}s: {len(response.get('message', {}).get('content', ''))} ký tự"
            )

            content = response.get("message", {}).get("content", "")
            if not content:
                return "❌ Không nhận được phản hồi từ AI (response rỗng)"

            return str(content)

        except Exception as e:
            self.logger.error(f"Lỗi chat: {e}")
            return f"❌ Lỗi chat: {e}"

    def review_code(self, file_path: str) -> str:
        """Review code file."""
        if not self.validate_file_path(file_path):
            return ERROR_INVALID_PATH.format(file_path)

        if not os.path.exists(file_path):
            return ERROR_FILE_NOT_FOUND.format(file_path)

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                code = f.read()

            prompt = f"""
            Review Python code và đưa ra nhận xét ngắn gọn:

            File: {file_path}

            Code:
            ```python
            {code}
            ```

            Tập trung vào:
            1. Code quality
            2. Performance issues
            3. Security concerns
            4. Best practices

            Trả lời ngắn gọn.
            """

            # Chạy chat
            result = self.chat(prompt)
            return result

        except Exception as e:
            self.logger.error(f"Lỗi đọc file: {e}")
            return f"❌ Lỗi đọc file: {e}"

    def optimize_code(self, file_path: str) -> str:
        """Optimize code."""
        if not self.validate_file_path(file_path):
            return ERROR_INVALID_PATH.format(file_path)

        if not os.path.exists(file_path):
            return ERROR_FILE_NOT_FOUND.format(file_path)

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                code = f.read()

            prompt = f"""
            Hãy optimize code sau đây:

            File: {file_path}
            Language: {Path(file_path).suffix}

            Code:
            ```{Path(file_path).suffix[1:]}
            {code}
            ```

            Yêu cầu:
            1. Cải thiện performance
            2. Giảm complexity
            3. Tối ưu memory usage
            4. Cải thiện readability
            5. Thêm type hints nếu là Python
            6. Error handling tốt hơn

            Trả về code đã optimize với giải thích thay đổi.
            """

            # Chạy chat
            result = self.chat(prompt)
            return result

        except Exception as e:
            self.logger.error(f"Lỗi đọc file: {e}")
            return f"❌ Lỗi đọc file: {e}"

    def generate_tests(self, file_path: str) -> str:
        """Generate unit tests."""
        if not self.validate_file_path(file_path):
            return ERROR_INVALID_PATH.format(file_path)

        if not os.path.exists(file_path):
            return ERROR_FILE_NOT_FOUND.format(file_path)

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                code = f.read()

            prompt = f"""
            Hãy tạo unit tests cho code sau đây:

            File: {file_path}
            Language: {Path(file_path).suffix}

            Code:
            ```{Path(file_path).suffix[1:]}
            {code}
            ```

            Yêu cầu:
            1. Test coverage cao
            2. Test cases cho normal và edge cases
            3. Mock external dependencies
            4. Assertions rõ ràng
            5. Test naming conventions
            6. Setup và teardown proper

            Trả về test code hoàn chỉnh.
            """

            # Chạy chat
            result = self.chat(prompt)
            return result

        except Exception as e:
            self.logger.error(f"Lỗi đọc file: {e}")
            return f"❌ Lỗi đọc file: {e}"


def check_dependencies() -> bool:
    """Kiểm tra dependencies cần thiết."""
    print("🔍 Kiểm tra dependencies...")

    # Check Python
    print(f"✅ Python: {sys.version}")

    # Check Ollama
    try:
        result = subprocess.run(["ollama", "--version"], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ Ollama: {result.stdout.strip()}")
        else:
            print("❌ Ollama không tìm thấy")
            return False
    except FileNotFoundError:
        print("❌ Ollama không có trong PATH")
        return False

    # Check Node.js (optional cho TypeScript support)
    try:
        result = subprocess.run(["node", "--version"], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ Node.js: {result.stdout.strip()}")
        else:
            print("⚠️  Node.js không tìm thấy")
    except FileNotFoundError:
        print("⚠️  Node.js không tìm thấy (chỉ cần nếu xử lý TypeScript)")

    # Check npm (optional)
    try:
        result = subprocess.run(["npm", "--version"], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ npm: {result.stdout.strip()}")
        else:
            print("⚠️  npm không tìm thấy")
    except FileNotFoundError:
        print("⚠️  npm không tìm thấy (chỉ cần nếu xử lý TypeScript)")

    return True


def setup_argument_parser() -> argparse.ArgumentParser:
    """Tạo argument parser với đầy đủ options."""
    parser = argparse.ArgumentParser(
        description="DeepSeek R1 Agent Terminal Runner",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python run_deepseek_agent.py chat "Hello, how are you?"
  python run_deepseek_agent.py review demo.py
  python run_deepseek_agent.py review --file demo.py
  python run_deepseek_agent.py optimize demo.py --verbose
  python run_deepseek_agent.py test --file demo.py
  python run_deepseek_agent.py setup
        """,
    )

    # Subcommands
    subparsers = parser.add_subparsers(dest="command", help="Commands")

    # Chat command
    chat_parser = subparsers.add_parser("chat", help="Chat with AI agent")
    chat_parser.add_argument("message", help="Message cho chat")

    # File-based commands
    for cmd in ["review", "optimize", "test"]:
        cmd_parser = subparsers.add_parser(cmd, help=f"{cmd.capitalize()} code file")
        cmd_parser.add_argument("file", help="Đường dẫn file để xử lý")
        cmd_parser.add_argument(
            "--verbose", "-v", action="store_true", help="Hiển thị thông tin chi tiết"
        )

    # Setup command
    subparsers.add_parser("setup", help="Kiểm tra setup")

    # Global options
    parser.add_argument(
        "--model",
        default="gpt-oss:20b",
        help="Ollama model để sử dụng (gpt-oss:20b, deepseek-coder:1.3b, deepseek-r1:8b)",
    )
    parser.add_argument("--url", default="http://127.0.0.1:11434", help="Ollama server URL")

    return parser


def handle_chat_command(agent: DeepSeekAgent, args: argparse.Namespace) -> None:
    """Xử lý chat command."""
    print(f"🤖 Chat: {args.message}")
    print("-" * 50)
    response = agent.chat(args.message)
    print(response)


def handle_file_command(agent: DeepSeekAgent, args: argparse.Namespace, command_type: str) -> None:
    """Xử lý các command liên quan đến file."""
    command_info = {
        "review": ("🔍 Reviewing", agent.review_code),
        "optimize": ("⚡ Optimizing", agent.optimize_code),
        "test": ("🧪 Generating tests for", agent.generate_tests),
    }

    emoji, func = command_info[command_type]
    print(f"{emoji}: {args.file} (using {agent.model})")
    print("-" * 50)

    try:
        print("⏳ Đang xử lý, vui lòng đợi... (có thể mất 1-2 phút với model lớn)")
        response = func(args.file)
        print("✅ Hoàn thành!")
        print()

        if response:
            print(response)
        else:
            print("❌ Không nhận được phản hồi từ AI")
    except Exception as e:
        print(f"❌ Lỗi xử lý file: {e}")
        if getattr(args, "verbose", False):
            import traceback

            traceback.print_exc()


def main() -> None:
    """Main function."""
    try:
        parser = setup_argument_parser()
        args = parser.parse_args()

        if not hasattr(args, "command"):
            parser.print_help()
            return

        # Check dependencies
        if not check_dependencies():
            print("\n❌ Thiếu dependencies. Vui lòng cài đặt trước.")
            return

        # Initialize agent
        verbose = getattr(args, "verbose", False)
        agent = DeepSeekAgent(model=args.model, base_url=args.url, verbose=verbose)

        # Check Ollama connection
        if not agent.check_ollama_connection():
            print(f"\n{ERROR_CONNECTION_FAILED}")
            print("💡 Khởi động Ollama: ollama serve")
            print("💡 Tải model: ollama pull deepseek-r1:latest")
            return

        print(f"✅ Kết nối Ollama thành công ({args.model})")
        if verbose:
            print(f"📡 Server URL: {args.url}")
        print()

        # Execute command
        if args.command == "setup":
            print("🚀 Setup hoàn tất! Agent sẵn sàng sử dụng.")
        elif args.command == "chat":
            handle_chat_command(agent, args)
        elif args.command in ["review", "optimize", "test"]:
            handle_file_command(agent, args, args.command)

    except KeyboardInterrupt:
        print("\n\n⚠️  Đã dừng bởi người dùng")
    except Exception as e:
        print(f"\n❌ Lỗi không mong muốn: {e}")
        if verbose:
            import traceback

            traceback.print_exc()


if __name__ == "__main__":
    main()
