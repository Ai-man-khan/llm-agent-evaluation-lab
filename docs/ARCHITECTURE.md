# Architecture

This repository uses a deliberately small evaluation architecture so the public example is easy to audit.

```text
                 +----------------------+
                 | candidate workspace  |
                 +----------+-----------+
                            |
                            | added to PYTHONPATH only
                            v
+-------------+     +-------+--------+      +------------------+
| grader tests| --> | evaluator      | ---> | structured result|
| outside     |     | subprocess run |      | status + logs    |
| candidate   |     +----------------+      +------------------+
+-------------+
```

## Separation

The candidate directory contains only code the hypothetical agent may modify. The grader directory is outside that workspace. The runner executes the grader with the candidate importable through `PYTHONPATH`.

This is a demonstration boundary, not a hardened security sandbox. A production system should use stronger isolation such as containers or VMs, resource limits, filesystem restrictions, network policy, and immutable grader assets.

## Controls

The demo evaluates three candidates against the same grader:

- **reference** — known-good implementation; expected to pass
- **starter** — intentionally buggy implementation; expected to fail
- **no-op** — deliberately deficient implementation; expected to fail

Control outcomes help distinguish a useful grader from one that always passes or always fails.

## Result record

Each run records:

- candidate and grader paths
- executed command
- pass/fail status
- exit code
- timeout status
- elapsed time
- stdout
- stderr

No user credentials, provider tokens, raw LLM prompts, or private model trajectories are collected by this example.
