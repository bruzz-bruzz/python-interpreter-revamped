"""Built-in functions available to interpreted programs."""

from typing import Any, Callable, Dict


class BuiltInFunctions:
    """Container for all built-in functions."""

    @staticmethod
    def _print(*args: Any) -> None:
        """Print arguments separated by spaces, with a trailing newline."""
        print(*args)

    @staticmethod
    def _len(obj: Any) -> int:
        """Return the length of an object."""
        return len(obj)

    @staticmethod
    def _range(*args: int):
        """Mimic Python's range() builtin."""
        return range(*args)

    @staticmethod
    def _str(obj: Any) -> str:
        """Return the string representation of obj."""
        return str(obj)

    @staticmethod
    def _int(obj: Any) -> int:
        """Convert obj to int."""
        return int(obj)

    @staticmethod
    def _float(obj: Any) -> float:
        """Convert obj to float."""
        return float(obj)

    @staticmethod
    def _type(obj: Any) -> str:
        """Return the type name of obj."""
        if obj is None:
            return "NoneType"
        if isinstance(obj, bool):
            return "bool"
        if isinstance(obj, int):
            return "int"
        if isinstance(obj, float):
            return "float"
        if isinstance(obj, str):
            return "str"
        if isinstance(obj, list):
            return "list"
        if isinstance(obj, dict):
            return "dict"
        return type(obj).__name__

    @classmethod
    def all_functions(cls) -> Dict[str, Callable]:
        """Return a name->function mapping for every built-in."""
        return {
            "print": cls._print,
            "len": cls._len,
            "range": cls._range,
            "str": cls._str,
            "int": cls._int,
            "float": cls._float,
            "type": cls._type,
        }
