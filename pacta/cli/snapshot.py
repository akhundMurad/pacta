from pathlib import Path

from pacta.cli._io import ensure_repo_root
from pacta.core.config import EngineConfig
from pacta.core.engine import DefaultPactaEngine
from pacta.snapshot.builder import DefaultSnapshotBuilder
from pacta.snapshot.store import FsSnapshotStore
from pacta.snapshot.types import SnapshotMeta


def save(
    *,
    path: str,
    ref: str,
    model: str | None,
    tool_version: str | None,
) -> int:
    """
    Save architecture snapshot under ref.

    This captures the current architecture structure (nodes, edges) WITHOUT
    running rules evaluation. Use this for:
      - Creating architecture snapshots for diffing
      - Tracking architecture evolution over time

    For creating baselines with violations, use `pacta baseline create` instead.

    Args:
        path: Repository root path
        ref: Snapshot reference name (default: "latest")
        model: Architecture model file path (optional, for enrichment)
        tool_version: Tool version for metadata
    """
    repo_root = Path(ensure_repo_root(path))

    # Build engine config (no rules - just architecture analysis)
    model_file: Path | None = None
    if model:
        model_file = Path(model)
        if not model_file.is_absolute():
            model_file = repo_root / model_file

    cfg = EngineConfig(
        repo_root=repo_root,
        rules_files=(),  # No rules for snapshot save
        model_file=model_file,
        deterministic=True,
    )

    # Build IR without running rules
    engine = DefaultPactaEngine()
    ir = engine.build_ir(cfg)

    # Build and save snapshot (no violations)
    meta = SnapshotMeta(repo_root=str(repo_root), tool_version=tool_version)
    snap = DefaultSnapshotBuilder().build(ir, meta=meta)

    store = FsSnapshotStore(repo_root=str(repo_root))
    written = store.save(snap, ref)

    print(f"Saved snapshot: {written}")
    print(f"  Nodes: {len(snap.nodes)}")
    print(f"  Edges: {len(snap.edges)}")

    return 0
