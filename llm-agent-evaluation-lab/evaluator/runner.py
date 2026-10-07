from __future__ import annotations

import os
from pathlib import Path
import subprocess
import sys
import time

from .result import EvaluationResult


def evaluate_candidate(
    candidate: str | Path,
    tests: str | Path,
    *,
    timeout_seconds: float = 10.0,
) -> EvaluationResult:
    """Run unittest-based grader tests against a candidate workspace.

    The grader directory is kept outside the candidate workspace. The candidate
    is made importable only through PYTHONPATH, which demonstrates a basic
    separation between submitted code and verifier code.
    """

    candidate_path = Path(candidate).resolve()
    tests_path = Path(tests).resolve()

    if not candidate_path.is_dir():
        raise ValueError(f"candidate directory does not exist: {candidate_path}")
    if not tests_path.is_dir():
        raise ValueError(f"tests directory does not exist: {tests_path}")

    env = os.environ.copy()
    existing = env.get("PYTHONPATH")
    env["PYTHONPATH"] = (
        str(candidate_path)
        if not existing
        else os.pathsep.join([str(candidate_path), existing])
    )

    command = [
        sys.executable,
        "-m",
        "unittest",
        "discover",
        "-s",
        str(tests_path),
        "-p",
        "test_*.py",
        "-v",
    ]

    started = time.monotonic()
    try:
        completed = subprocess.run(
            command,
            cwd=tests_path.parent,
            env=env,
            text=True,
            capture_output=True,
            timeout=timeout_seconds,
            check=False,
        )
        duration = time.monotonic() - started
        return EvaluationResult(
            candidate=str(candidate_path),
            tests=str(tests_path),
            command=command,
            passed=completed.returncode == 0,
            exit_code=completed.returncode,
            timed_out=False,
            duration_seconds=round(duration, 6),
            stdout=completed.stdout,
            stderr=completed.stderr,
        )
    except subprocess.TimeoutExpired as exc:
        duration = time.monotonic() - started
        stdout = exc.stdout or ""
        stderr = exc.stderr or ""
        if isinstance(stdout, bytes):
            stdout = stdout.decode(errors="replace")
        if isinstance(stderr, bytes):
            stderr = stderr.decode(errors="replace")
        return EvaluationResult(
            candidate=str(candidate_path),
            tests=str(tests_path),
            command=command,
            passed=False,
            exit_code=None,
            timed_out=True,
            duration_seconds=round(duration, 6),
            stdout=stdout,
            stderr=stderr,
        )
