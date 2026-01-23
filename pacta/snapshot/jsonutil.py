import json
from collections.abc import Mapping
from dataclasses import asdict, is_dataclass
from pathlib import Path
from typing import Any


def _is_pydantic_model(obj: Any) -> bool:
    # pydantic v1: .dict() ; pydantic v2: .model_dump()
    return hasattr(obj, "model_dump") or hasattr(obj, "dict")


def to_jsonable(obj: Any) -> Any:
    """
    Convert common Python objects to JSON-serializable structures.
    Deterministic and safe for dataclasses/pydantic/Path.
    """
    if obj is None:
        return None

    if isinstance(obj, (str, int, float, bool)):
        return obj

    if isinstance(obj, Path):
        return str(obj)

    if isinstance(obj, Mapping):
        # sort keys for determinism
        return {str(k): to_jsonable(obj[k]) for k in sorted(obj.keys(), key=lambda x: str(x))}

    if isinstance(obj, (list, tuple, set, frozenset)):
        return [to_jsonable(v) for v in obj]

    if is_dataclass(obj):
        return to_jsonable(asdict(obj))

    if _is_pydantic_model(obj):
        if hasattr(obj, "model_dump"):
            return to_jsonable(obj.model_dump())
        return to_jsonable(obj.dict())

    # Fallback: attempt to serialize __dict__ then repr
    if hasattr(obj, "__dict__"):
        return to_jsonable(vars(obj))

    return repr(obj)


def dumps_deterministic(data: Any) -> str:
    """
    Deterministic JSON string:
    - sorted keys
    - no whitespace
    """
    return json.dumps(to_jsonable(data), sort_keys=True, separators=(",", ":"), ensure_ascii=False, indent=4)


def dump_file(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(dumps_deterministic(data) + "\n", encoding="utf-8")


def load_file(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))
