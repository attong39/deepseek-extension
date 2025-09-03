"""
Demo Python file để test DeepSeek Agent
"""


def calculate_fibonacci(n: int) -> int:
    """Tính số Fibonacci thứ n."""
    if n <= 1:
        return n
    return calculate_fibonacci(n - 1) + calculate_fibonacci(n - 2)


def is_prime(num: int) -> bool:
    """Kiểm tra số nguyên tố."""
    if num <= 1:
        return False
    for i in range(2, int(num**0.5) + 1):
        if num % i == 0:
            return False
    return True


class Calculator:
    """Simple calculator class."""

    def add(self, a: float, b: float) -> float:
        """Cộng hai số."""
        return a + b

    def multiply(self, a: float, b: float) -> float:
        """Nhân hai số."""
        return a * b


if __name__ == "__main__":
    # Test functions
    print(f"Fibonacci(10): {calculate_fibonacci(10)}")
    print(f"Is 17 prime? {is_prime(17)}")

    calc = Calculator()
    print(f"5 + 3 = {calc.add(5, 3)}")
    print(f"5 * 3 = {calc.multiply(5, 3)}")
