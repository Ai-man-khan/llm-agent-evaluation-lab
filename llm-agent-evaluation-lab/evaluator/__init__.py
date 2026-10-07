"""Generic, public-safe agent evaluation helpers."""

from .result import EvaluationResult
from .runner import evaluate_candidate

__all__ = ["EvaluationResult", "evaluate_candidate"]
