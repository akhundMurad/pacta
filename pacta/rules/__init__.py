from pathlib import Path

from pacta.rules.ast import (
    AndAst,
    CompareAst,
    DependencyWhenAst,
    ExprAst,
    FieldAst,
    LiteralAst,
    NodeWhenAst,
    NotAst,
    OrAst,
    RuleAst,
    RulesDocumentAst,
    WhenAst,
)
from pacta.rules.baseline import BaselineComparer, BaselineResult, ViolationKeyStrategy
from pacta.rules.compiler import RulesCompiler
from pacta.rules.dsl import DefaultDSLParser
from pacta.rules.errors import RulesCompileError, RulesError, RulesEvalError, RulesParseError
from pacta.rules.evaluator import DefaultRuleEvaluator, RuleEvaluatorProtocol
from pacta.rules.explain import explain_rule, explain_violation
from pacta.rules.loader import DefaultRuleSourceLoader, RuleSource
from pacta.rules.parser import DslRulesParserV0, RulesParser
from pacta.rules.types import Rule, RuleAction, RuleSet, RuleTarget

__all__ = [
    # AST
    "RulesDocumentAst",
    "RuleAst",
    "WhenAst",
    "DependencyWhenAst",
    "NodeWhenAst",
    "ExprAst",
    "AndAst",
    "OrAst",
    "NotAst",
    "CompareAst",
    "FieldAst",
    "LiteralAst",
    # Runtime types
    "Rule",
    "RuleAction",
    "RuleTarget",
    "RuleSet",
    # Parsing / compiling
    "RulesParser",
    "DslRulesParserV0",
    "DefaultDSLParser",
    "RulesCompiler",
    # Loading
    "DefaultRuleSourceLoader",
    "RuleSource",
    # Evaluation
    "RuleEvaluatorProtocol",
    "DefaultRuleEvaluator",
    # Baseline
    "ViolationKeyStrategy",
    "BaselineComparer",
    "BaselineResult",
    # Explain
    "explain_rule",
    "explain_violation",
    # Errors
    "RulesError",
    "RulesParseError",
    "RulesCompileError",
    "RulesEvalError",
]

# Convenience helpers (public API)


def load_rules(path: str | Path):
    """
    Load and compile rules from a file.

    Currently uses the v0 DSL parser.
    """
    parser = DslRulesParserV0()
    compiler = RulesCompiler()

    doc = parser.parse_file(path)
    return compiler.compile(doc)


def evaluate(ir, rules: RuleSet):
    """
    Evaluate compiled rules against IR or IRIndex.
    """
    evaluator = DefaultRuleEvaluator()
    return evaluator.evaluate(ir, rules)
