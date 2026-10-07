# LLM Agent Evaluation Lab

A **public-safe, clean-room portfolio repository** for demonstrating how terminal-based coding agents can be evaluated in reproducible sandboxes.

This repository intentionally contains only generic evaluation code and a fully synthetic task. It does **not** contain private Terminal-Bench task bundles, hidden tests, reference solutions from non-public tasks, model trajectories, internal authoring prompts, reviewer notes, credentials, or company-owned workflow material.

> **Status:** Independent portfolio project. Not an official Terminal-Bench, Harbor, Mercor, AirDawg Labs, or Caudal AI repository.

## What this demonstrates

- Reproducible candidate evaluation from a clean working directory
- Separation between the candidate workspace and grader tests
- Timeout and process-output capture
- Positive and negative controls
- Structured JSON evaluation results
- A synthetic stateful engineering task with a reference implementation
- A publication boundary that prevents accidental disclosure of private benchmark material

## Repository layout

```text
llm-agent-evaluation-lab/
├── evaluator/                         # Generic evaluation runner
│   ├── cli.py                         # CLI: evaluate or run the demo matrix
│   ├── controls.py                    # Positive/negative control helpers
│   ├── result.py                      # Structured result model
│   └── runner.py                      # Isolated subprocess execution
├── examples/
│   └── synthetic-lease-registry/
│       ├── instruction.md             # Public task contract
│       ├── task.json                  # Demo task metadata
│       ├── workspace/                 # Intentionally buggy starter code
│       ├── grader/                    # Synthetic verifier tests
│       ├── reference/                 # Synthetic positive control
│       └── no_op/                     # Synthetic negative control
├── tests/                             # Tests for this public evaluator
├── docs/
│   ├── ARCHITECTURE.md
│   ├── PRIVATE_BOUNDARY.md            # What must not be copied from private work
│   └── PUBLICATION_CHECKLIST.md
└── scripts/demo.sh
```

## Quick start

Requirements: Python 3.11+.

```bash
python -m evaluator.cli demo
```

Expected high-level outcome:

```text
reference   PASS
starter     FAIL
no-op       FAIL
```

Run the evaluator against one candidate directly:

```bash
python -m evaluator.cli evaluate \
  --candidate examples/synthetic-lease-registry/workspace \
  --tests examples/synthetic-lease-registry/grader
```

The command prints a JSON report containing the exit code, duration, captured output, and pass/fail status.

## Evaluation model

The public evaluator follows a small, generic control loop:

1. **Candidate workspace** — code being evaluated.
2. **Grader** — tests stored outside the candidate workspace.
3. **Runner** — launches the grader with the candidate on `PYTHONPATH`.
4. **Positive control** — a known-good synthetic reference should pass.
5. **Negative control** — a no-op implementation should fail.
6. **Result record** — command, duration, exit code, stdout/stderr, and status are recorded.

This is deliberately smaller than a production agent-evaluation platform. It is meant to show the engineering principles without publishing any private benchmark infrastructure.

## Synthetic example: fenced lease registry

The example task models a small ownership/lease component. A caller can acquire a resource, renew it, and release it using a monotonically increasing fencing token. Expired or stale owners must not be able to mutate the current lease.

The starter implementation contains several defects. The grader checks observable behavior rather than requiring a specific internal implementation.

See [`examples/synthetic-lease-registry/instruction.md`](examples/synthetic-lease-registry/instruction.md).

## Public/private boundary

Before adding anything from real benchmark work, read [`docs/PRIVATE_BOUNDARY.md`](docs/PRIVATE_BOUNDARY.md). The safest rule is:

> If a file came from an employer/client workspace, a private benchmark authoring repository, an unreleased task, an internal portal, a model-evaluation run, or a reviewer, do not publish it unless you have explicit redistribution permission.

This repository's `.gitignore` also blocks common private-artifact paths and secret files as a second line of defense.

## What to show recruiters instead of private artifacts

Use clean-room demonstrations like this repository to explain skills such as:

- task-contract design
- verifier/test quality
- reproducible sandboxes
- failure classification
- positive and negative controls
- trajectory/log analysis concepts
- timeout handling
- evidence-backed evaluation

Describe outcomes at a high level without uploading private task implementations, exact hidden tests, confidential prompts, or raw model traces.

## Testing this repository

```bash
python -m unittest discover -s tests -v
```

## License

The code authored specifically for this clean-room example is released under the MIT License. That license does **not** grant rights to any third-party, employer-owned, benchmark-owned, or otherwise private material that is intentionally excluded from this repository.
