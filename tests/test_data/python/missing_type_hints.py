"""Missing Type Hints module."""


def untyped_function(param):  # Should detect missing type hints
    return param + 1


class UntypedClass:
    def method(self, value):  # Should detect missing type hints
        return value
import param
import value
