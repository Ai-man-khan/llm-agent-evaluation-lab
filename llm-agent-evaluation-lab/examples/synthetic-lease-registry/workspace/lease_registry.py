class LeaseBusy(RuntimeError):
    pass


class StaleLease(RuntimeError):
    pass


class LeaseRegistry:
    """Intentionally buggy starter implementation for the public demo."""

    def __init__(self, clock):
        self._clock = clock
        self._leases = {}

    def acquire(self, key, owner, ttl):
        if ttl <= 0:
            raise ValueError("ttl must be positive")
        current = self._leases.get(key)
        if current and current["expires_at"] > self._clock():
            raise LeaseBusy(key)
        # BUG: fencing token is reset instead of remaining monotonic.
        token = 1
        self._leases[key] = {
            "owner": owner,
            "token": token,
            "expires_at": self._clock() + ttl,
        }
        return token

    def renew(self, key, owner, token, ttl):
        if ttl <= 0:
            raise ValueError("ttl must be positive")
        current = self._leases.get(key)
        if not current:
            raise StaleLease(key)
        # BUG: does not validate owner/token or expiry.
        current["expires_at"] = self._clock() + ttl
        return current["token"]

    def release(self, key, owner, token):
        # BUG: stale owners can release the active lease.
        if key not in self._leases:
            raise StaleLease(key)
        del self._leases[key]

    def current(self, key):
        # BUG: expired leases are still returned.
        current = self._leases.get(key)
        return dict(current) if current else None
