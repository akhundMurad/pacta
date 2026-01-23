from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class EngineConfig:
    repo_root: Path
    model_file: Path | None
    rules_files: tuple[Path, ...]
    baseline: str | None = None
    changed_only: bool = False
    include_paths: tuple[Path, ...] = ()
    exclude_globs: tuple[str, ...] = ()
    output_format: str = "text"
    deterministic: bool = True
    save_ref: str | None = None  # Save snapshot under this ref (in addition to "latest")
