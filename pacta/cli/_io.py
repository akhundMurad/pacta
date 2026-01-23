from pathlib import Path


def ensure_repo_root(path: str) -> str:
    p = Path(path).resolve()
    if not p.exists():
        raise FileNotFoundError(f"Path does not exist: {p}")
    return str(p)


def default_rules_files(repo_root: str) -> tuple[str, ...]:
    p = Path(repo_root)
    candidate = p / "pacta.rules"
    return (str(candidate),) if candidate.exists() else ()


def default_model_file(repo_root: str) -> str | None:
    p = Path(repo_root)
    candidate = p / "architecture.yaml"
    return str(candidate) if candidate.exists() else None
