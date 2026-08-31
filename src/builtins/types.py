"""Built-in type names exposed to interpreted programs.

We rely on Python's native types directly; this module just provides a
consistent registration surface for the interpreter.
"""

from typing import Any, Dict


class BuiltInTypes:
    """Container for built-in type objects."""

    @classmethod
    def all_types(cls) -> Dict[str, Any]:
        """Return a name->type mapping for every built-in type."""
        return {
            "int": int,
            "float": float,
            "str": str,
            "bool": bool,
            "list": list,
            "dict": dict,
            "tuple": tuple,
            "set": set,
            "NoneType": type(None),
        }
