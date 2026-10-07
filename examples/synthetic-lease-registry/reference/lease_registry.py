class LeaseBusy(RuntimeError):
    pass


class StaleLease(RuntimeError):
    pass


class LeaseRegistry:
    def __init__(self, clock):
        self._clock = clock
        self._leases = {}
        self._last_token = {}

    def _active(self, key):
        lease = self._leases.get(key)
        if lease is None:
            return None
        if lease["expires_at"] <= self._clock():
            del self._leases[key]
            return None
        return lease

    @staticmethod
    def _validate_ttl(ttl):
        if ttl <= 0:
            raise ValueError("ttl must be positive")

    def acquire(self, key, owner, ttl):
        self._validate_ttl(ttl)
        if self._active(key) is not None:
            raise LeaseBusy(key)
        token = self._last_token.get(key, 0) + 1
        self._last_token[key] = token
        self._leases[key] = {
            "owner": owner,
            "token": token,
            "expires_at": self._clock() + ttl,
        }
        return token

    def renew(self, key, owner, token, ttl):
        self._validate_ttl(ttl)
        lease = self._active(key)
        if lease is None or lease["owner"] != owner or lease["token"] != token:
            raise StaleLease(key)
        lease["expires_at"] = self._clock() + ttl
        return lease["token"]

    def release(self, key, owner, token):
        lease = self._active(key)
        if lease is None or lease["owner"] != owner or lease["token"] != token:
            raise StaleLease(key)
        del self._leases[key]

    def current(self, key):
        lease = self._active(key)
        return dict(lease) if lease is not None else None
