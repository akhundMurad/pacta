from pacta.cli._io import ensure_repo_root
from pacta.snapshot.diff import DefaultSnapshotDiffEngine
from pacta.snapshot.store import FsSnapshotStore


def snapshot_diff(*, path: str, from_ref: str, to_ref: str) -> int:
    repo_root = ensure_repo_root(path)
    store = FsSnapshotStore(repo_root=repo_root)

    before = store.load(from_ref)
    after = store.load(to_ref)

    d = DefaultSnapshotDiffEngine().diff(before, after, include_details=True)

    print("Snapshot diff:")
    print(f"  nodes: +{d.nodes_added}  -{d.nodes_removed}")
    print(f"  edges: +{d.edges_added}  -{d.edges_removed}")

    # Optional details counts
    if d.details:
        nodes = d.details.get("nodes", {})
        edges = d.details.get("edges", {})
        if nodes.get("added"):
            print(f"  nodes added: {len(nodes['added'])}")
        if nodes.get("removed"):
            print(f"  nodes removed: {len(nodes['removed'])}")
        if nodes.get("changed"):
            print(f"  nodes changed: {len(nodes['changed'])}")
        if edges.get("added"):
            print(f"  edges added: {len(edges['added'])}")
        if edges.get("removed"):
            print(f"  edges removed: {len(edges['removed'])}")
        if edges.get("changed"):
            print(f"  edges changed: {len(edges['changed'])}")

    return 0
