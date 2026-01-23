from collections.abc import Mapping
from dataclasses import dataclass
from typing import Any

from pacta.reporting.types import Violation
from pacta.rules.types import Rule, RuleTarget

# Human-readable explanations


def explain_violation(v: Violation) -> str:
    """
    Turn a Violation into a human-readable explanation suitable for CLI/IDE tooltips.
    """
    ctx = v.context or {}
    target = ctx.get("target")

    if target == "dependency":
        dep_type = ctx.get("dep_type", "dependency")
        src = ctx.get("src_fqname") or ctx.get("src_id") or "unknown"
        dst = ctx.get("dst_fqname") or ctx.get("dst_id") or "unknown"
        src_layer = ctx.get("src_layer")
        dst_layer = ctx.get("dst_layer")

        # Build natural language explanation
        verb = _dep_type_verb(dep_type)

        if src_layer and dst_layer:
            return f'"{src}" in {src_layer} layer {verb} "{dst}" in {dst_layer} layer'
        else:
            return f'"{src}" {verb} "{dst}"'

    if target == "node":
        ident = ctx.get("fqname") or ctx.get("node_id") or "unknown"
        kind = ctx.get("kind", "element")
        layer = ctx.get("layer")
        context_name = ctx.get("context")
        container = ctx.get("container")

        # Build natural language explanation
        location_parts = []
        if layer:
            location_parts.append(f"{layer} layer")
        if container:
            location_parts.append(f"container {container}")
        if context_name:
            location_parts.append(f"context {context_name}")

        if location_parts:
            location = ", ".join(location_parts)
            return f'{kind} "{ident}" found in {location}'
        else:
            return f'{kind} "{ident}" violates architectural constraint'

    # Fallback
    return v.message


def _dep_type_verb(dep_type: str) -> str:
    """Convert dependency type to a human-readable verb."""
    verbs = {
        "import": "imports",
        "call": "calls",
        "inherit": "inherits from",
        "instantiate": "instantiates",
        "use": "uses",
        "reference": "references",
    }
    return verbs.get(dep_type, f"depends on ({dep_type})")


def explain_rule(rule: Rule) -> str:
    """
    Explain a compiled Rule at a high level (for listing rules, debug output).
    """
    target = "dependencies" if rule.target == RuleTarget.DEPENDENCY else "nodes"
    action = rule.action.value.lower()

    base = f"[{rule.id}] {rule.name} — {action} {target} ({rule.severity.value.lower()})"
    if rule.description:
        return f"{base}\n{rule.description}"
    return base


# Optional: "why did it match?" debug helpers (v0)


@dataclass(frozen=True, slots=True)
class PredicateTrace:
    """
    Minimal trace record for debugging predicate evaluation.
    """

    rule_id: str
    matched: bool
    details: Mapping[str, Any]


def trace_violation(v: Violation) -> PredicateTrace:
    """
    v0 trace: just echo violation context.
    Future: include expression tree and extracted field values.
    """
    return PredicateTrace(
        rule_id=v.rule.id,
        matched=True,
        details=v.context or {},
    )
