from __future__ import annotations

from pathlib import Path

from .result import EvaluationResult
from .runner import evaluate_candidate


def run_control_matrix(task_root: str | Path, timeout_seconds: float = 10.0) -> dict[str, EvaluationResult]:
    """Evaluate a known-good reference, buggy starter, and no-op control."""

    root = Path(task_root).resolve()
    tests = root / "grader"
    candidates = {
        "reference": root / "reference",
        "starter": root / "workspace",
        "no-op": root / "no_op",
    }
    return {
        name: evaluate_candidate(path, tests, timeout_seconds=timeout_seconds)
        for name, path in candidates.items()
    }
