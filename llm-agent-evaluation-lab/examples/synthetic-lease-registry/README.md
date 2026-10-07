# Synthetic lease-registry task

This task is entirely synthetic and was created for this public portfolio repository.

- `workspace/` is the intentionally buggy starter candidate.
- `grader/` is separate from the candidate and checks only the public contract.
- `reference/` is a known-good positive control authored for this example.
- `no_op/` is a deliberately deficient negative control.

Run all controls from the repository root:

```bash
python -m evaluator.cli demo
```
