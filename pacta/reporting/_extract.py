from collections.abc import Mapping
from typing import Any


def get_field(obj: Any, *names: str, default: Any = None) -> Any:
    """
    Read a field from either:
    - Mapping (dict-like)
    - object attributes

    Tries names in order. Returns default if not found.
    """
    if obj is None:
        return default

    if isinstance(obj, Mapping):
        for n in names:
            if n in obj:
                return obj[n]
        return default

    for n in names:
        if hasattr(obj, n):
            return getattr(obj, n)
    return default
