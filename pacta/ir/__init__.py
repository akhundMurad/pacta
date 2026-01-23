# Core types (stable public API)

# Indexing & querying
from pacta.ir.index import (
    IRIndex,
    build_index,
)

# Identity / keys
from pacta.ir.keys import (
    dedupe_edges,
    dedupe_nodes,
    edge_key,
    node_key,
)

# IR processing
from pacta.ir.merge import DefaultIRMerger
from pacta.ir.normalize import DefaultIRNormalizer
from pacta.ir.select import (
    EdgeFilter,
    NodeFilter,
    match_glob,
    match_regex,
    select_edges,
    select_nodes,
)
from pacta.ir.types import (
    ArchitectureIR,
    CanonicalId,
    DepType,
    IREdge,
    IRNode,
    Language,
    SourceLoc,
    SourcePos,
    SymbolKind,
)

# Validation
from pacta.ir.validate import (
    IRValidationOptions,
    validate_ir,
)

# Public export control

__all__ = (
    # types
    "ArchitectureIR",
    "IRNode",
    "IREdge",
    "CanonicalId",
    "SourceLoc",
    "SourcePos",
    "Language",
    "SymbolKind",
    "DepType",
    # keys
    "node_key",
    "edge_key",
    "dedupe_nodes",
    "dedupe_edges",
    # processing
    "DefaultIRMerger",
    "DefaultIRNormalizer",
    # indexing
    "IRIndex",
    "build_index",
    # selection
    "NodeFilter",
    "EdgeFilter",
    "select_nodes",
    "select_edges",
    "match_glob",
    "match_regex",
    # validation
    "validate_ir",
    "IRValidationOptions",
)
