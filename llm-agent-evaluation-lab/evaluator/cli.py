from __future__ import annotations

import argparse
import json
from pathlib import Path

from .controls import run_control_matrix
from .runner import evaluate_candidate


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="agent-eval",
        description="Public-safe demonstration evaluator for coding-agent workspaces.",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    evaluate = sub.add_parser("evaluate", help="evaluate one candidate workspace")
    evaluate.add_argument("--candidate", required=True)
    evaluate.add_argument("--tests", required=True)
    evaluate.add_argument("--timeout", type=float, default=10.0)

    demo = sub.add_parser("demo", help="run reference/starter/no-op controls")
    demo.add_argument(
        "--task",
        default=str(
            Path(__file__).resolve().parents[1]
            / "examples"
            / "synthetic-lease-registry"
        ),
    )
    demo.add_argument("--timeout", type=float, default=10.0)
    demo.add_argument("--json", action="store_true", help="print full JSON reports")

    return parser


def main() -> int:
    args = _parser().parse_args()

    if args.command == "evaluate":
        result = evaluate_candidate(args.candidate, args.tests, timeout_seconds=args.timeout)
        print(result.to_json())
        return 0 if result.passed else 1

    results = run_control_matrix(args.task, timeout_seconds=args.timeout)
    if args.json:
        print(json.dumps({k: v.to_dict() for k, v in results.items()}, indent=2, sort_keys=True))
    else:
        for name, result in results.items():
            status = "PASS" if result.passed else "FAIL"
            suffix = " (timeout)" if result.timed_out else ""
            print(f"{name:<10} {status}{suffix}  {result.duration_seconds:.3f}s")

    # A healthy demo requires the positive control to pass and both deficient
    # candidates to fail.
    healthy = results["reference"].passed and not results["starter"].passed and not results["no-op"].passed
    return 0 if healthy else 2


if __name__ == "__main__":
    raise SystemExit(main())
