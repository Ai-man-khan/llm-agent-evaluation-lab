# Publication checklist

Run this checklist before making the repository public.

- [ ] Every source file in the repository was authored for this public project or is clearly redistributable.
- [ ] No real task bundle, unreleased `instruction.md`, hidden test, verifier, reference solution, or golden patch is present.
- [ ] No raw agent trajectory, model transcript, provider request/response log, or private reward artifact is present.
- [ ] No copied internal prompt, checklist, reviewer rubric, portal export, authoring skill, or audit tool is present.
- [ ] No API key, token, cookie, credential, `.env`, private key, or service-account file is present.
- [ ] No private organization URL, hostname, registry, project ID, job ID, or internal username remains.
- [ ] Git history does not contain files that were later deleted from the working tree.
- [ ] The synthetic example is clearly labeled synthetic.
- [ ] The repository states that it is independent and not an official benchmark/company repository.
- [ ] The license applies only to material you have the right to license.

## Suggested local checks

```bash
# Inspect what Git is about to publish.
git status --short
git ls-files

# Search tracked files for common secret names.
git grep -nEi 'api[_-]?key|access[_-]?token|secret|password|BEGIN .*PRIVATE KEY' || true

# Check for blocked private-workflow names.
git ls-files | grep -E '(^|/)(trajectories|oracle-nop-evidence|Task_Ready_To_Submit|docs/portal|prompts|solution)(/|$)' && \
  echo 'REVIEW: private-looking path found' || true
```

For a real public release, also use a dedicated secret scanner and review the full Git history, not only the current working tree.
