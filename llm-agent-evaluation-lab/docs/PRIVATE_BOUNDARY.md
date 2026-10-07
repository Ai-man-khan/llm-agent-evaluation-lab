# Private boundary: what must stay out of the public repository

This document is intentionally conservative. It is based on the layout of the private workflow archive used to plan this clean-room repository, plus standard secret/IP hygiene.

**Do not publish any item below unless you have explicit permission from the owner to redistribute it.** When ownership is uncertain, keep it private and publish a clean-room reimplementation instead.

## 1. Private task source and submissions

Keep private:

```text
tasks/
specs/
rubrics/
authoring/<real-task>/
Task_Ready_To_Submit/
*.zip containing real task bundles
```

Also keep private any unreleased real-task copies, staged task trees, or prior-task source copied from another benchmark workspace.

## 2. Reference solutions and answer material

Keep private for real/non-public tasks:

```text
solution/
solution/solve.sh
golden.patch
golden_patch.*
reference implementations
private answer keys
```

Do not publish a reference implementation just because the surrounding task description is safe to discuss.

## 3. Hidden/verifier-only evaluation material

Keep private for real/non-public tasks:

```text
hidden tests
held-out cases
private verifier data
tests or fixtures containing unreleased expected behavior
private reference files
grader-only secrets
```

A public synthetic grader is fine; a copied real verifier is not.

## 4. Evaluation evidence and model traces

Keep private unless publication is explicitly authorized:

```text
trajectories/
oracle-nop-evidence/
raw model/API logs
agent transcripts
Harbor/STB job outputs
ctrf.json from private evaluations
reward.txt / per-run rubric scores
step3c reports
failure screenshots or console logs containing private source
```

Even when a trace contains no credential, it can reveal task internals, system prompts, hidden tests, reviewer policy, or proprietary model-evaluation methodology.

## 5. Internal authoring workflow and policy material

The uploaded workflow archive contains detailed authoring/review infrastructure. Treat the following source paths as private by default unless you have redistribution rights:

```text
MASTER_CHECKLIST_TB4.0.md
TB4_CAPABILITY_HARDENING_RULES.md
TASK_PROPOSAL_RUBRIC.md
workflow-prompts.md
prompts/
.cursor/rules/
.cursor/skills/
docs/portal/
docs/prompts-for-others/
docs/reference/stb-full-fidelity-kit/
tools/final-tb4-audit-master/
authoring/_templates/
```

Do not copy text from these files into the public repository. Re-express only generic ideas in your own words and code.

## 6. Internal audit, packaging, and environment scripts

Do not publish copied versions of internal/private scripts such as authoring gates, packaging logic, fidelity capture, reviewer tooling, or environment patches unless their licensing and redistribution status is clear.

From the uploaded archive, that means treating the original `scripts/` tree as private-by-default rather than copying it wholesale. The `evaluator/` code in this public repository is a clean-room replacement written specifically for the portfolio example.

## 7. Credentials and machine-specific data

Never publish:

```text
.env / .env.*
API keys
access tokens
session cookies
STB/Harbor login material
cloud credentials
SSH/private keys
personal access tokens
service-account JSON
credential helper dumps
shell history containing secrets
```

Also remove machine-specific usernames, absolute home paths, internal hostnames, private registry names, and organization-only URLs where they reveal non-public infrastructure.

## 8. Reviewer and company information

Keep private unless already public and authorized:

- reviewer comments and audit findings tied to unreleased work
- internal team/member names in evaluation artifacts
- private Slack/email excerpts
- unpublished compensation/client details
- internal project IDs, job IDs, cohort IDs, or dashboard links

## 9. Safe substitutes for a portfolio

Instead of uploading the private material above, publish:

- a synthetic task you wrote from scratch
- a generic evaluator you wrote from scratch
- architecture diagrams with no internal endpoints
- sanitized screenshots containing only your public demo
- high-level case studies that describe the engineering problem without reproducing protected source, tests, prompts, or traces

## 10. Pre-push rule

If a file originated in the private workflow archive or a real task directory, **do not move it into this repository**. Recreate the concept from scratch in a new file and verify that it contains no copied passages, identifiers, secrets, hidden test data, or proprietary paths.
