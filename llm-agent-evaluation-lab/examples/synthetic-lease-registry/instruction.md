# Synthetic task: fenced lease registry

Implement the behavior of `LeaseRegistry` in `lease_registry.py`.

A registry manages at most one active lease for each resource key. A lease contains an owner, an expiry time, and a fencing token.

## Public contract

`LeaseRegistry(clock)` receives a zero-argument clock function that returns a numeric timestamp.

### `acquire(key, owner, ttl)`

- `ttl` must be greater than zero, otherwise raise `ValueError`.
- If the resource has no active lease, create one and return its fencing token.
- If the previous lease has expired, a new owner may acquire it.
- If the resource already has a non-expired lease, raise `LeaseBusy`.
- Every successful acquisition for a given key must return a token strictly greater than every token previously issued for that key, including after expiry or release.

### `renew(key, owner, token, ttl)`

- `ttl` must be greater than zero, otherwise raise `ValueError`.
- Renewal succeeds only when the lease is still active and both `owner` and `token` match the current lease.
- A stale owner, stale token, missing lease, or expired lease must raise `StaleLease`.
- A successful renewal extends expiry from the current clock time and returns the same fencing token.

### `release(key, owner, token)`

- Release succeeds only when `owner` and `token` match the current active lease.
- A stale owner, stale token, missing lease, or expired lease must raise `StaleLease`.
- A successful release removes the active lease but does not reset the token sequence.

### `current(key)`

Return `None` when there is no active lease. Otherwise return a dictionary with exactly:

```python
{"owner": <str>, "token": <int>, "expires_at": <number>}
```

An expired lease is treated as inactive.

## Constraints

- Keep the public class and exception names unchanged.
- Do not depend on network access or third-party packages.
- The grader evaluates observable behavior; no specific internal algorithm is required.
