class LeaseBusy(RuntimeError):
    pass


class StaleLease(RuntimeError):
    pass


class LeaseRegistry:
    """Deliberately deficient negative control."""

    def __init__(self, clock):
        self._clock = clock

    def acquire(self, key, owner, ttl):
        return 0

    def renew(self, key, owner, token, ttl):
        return token

    def release(self, key, owner, token):
        return None

    def current(self, key):
        return None
