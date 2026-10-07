import unittest

from lease_registry import LeaseBusy, LeaseRegistry, StaleLease


class Clock:
    def __init__(self, value=100.0):
        self.value = value

    def __call__(self):
        return self.value

    def advance(self, seconds):
        self.value += seconds


class LeaseRegistryTests(unittest.TestCase):
    def setUp(self):
        self.clock = Clock()
        self.registry = LeaseRegistry(self.clock)

    def test_acquire_and_current_shape(self):
        token = self.registry.acquire("gpu-1", "worker-a", 10)
        self.assertGreaterEqual(token, 1)
        self.assertEqual(
            self.registry.current("gpu-1"),
            {"owner": "worker-a", "token": token, "expires_at": 110.0},
        )

    def test_active_lease_blocks_second_acquire(self):
        self.registry.acquire("gpu-1", "worker-a", 10)
        with self.assertRaises(LeaseBusy):
            self.registry.acquire("gpu-1", "worker-b", 10)

    def test_token_increases_after_release(self):
        first = self.registry.acquire("gpu-1", "worker-a", 10)
        self.registry.release("gpu-1", "worker-a", first)
        second = self.registry.acquire("gpu-1", "worker-b", 10)
        self.assertGreater(second, first)

    def test_expired_lease_disappears_and_token_still_increases(self):
        first = self.registry.acquire("gpu-1", "worker-a", 3)
        self.clock.advance(4)
        self.assertIsNone(self.registry.current("gpu-1"))
        second = self.registry.acquire("gpu-1", "worker-b", 5)
        self.assertGreater(second, first)

    def test_stale_owner_cannot_renew_or_release(self):
        token = self.registry.acquire("gpu-1", "worker-a", 10)
        with self.assertRaises(StaleLease):
            self.registry.renew("gpu-1", "worker-b", token, 5)
        with self.assertRaises(StaleLease):
            self.registry.release("gpu-1", "worker-b", token)
        self.assertEqual(self.registry.current("gpu-1")["owner"], "worker-a")

    def test_stale_token_cannot_touch_new_lease(self):
        first = self.registry.acquire("gpu-1", "worker-a", 2)
        self.clock.advance(3)
        second = self.registry.acquire("gpu-1", "worker-b", 10)
        self.assertGreater(second, first)
        with self.assertRaises(StaleLease):
            self.registry.renew("gpu-1", "worker-a", first, 20)
        with self.assertRaises(StaleLease):
            self.registry.release("gpu-1", "worker-a", first)
        self.assertEqual(self.registry.current("gpu-1")["token"], second)

    def test_expired_lease_cannot_be_renewed_or_released(self):
        token = self.registry.acquire("gpu-1", "worker-a", 1)
        self.clock.advance(2)
        with self.assertRaises(StaleLease):
            self.registry.renew("gpu-1", "worker-a", token, 5)
        with self.assertRaises(StaleLease):
            self.registry.release("gpu-1", "worker-a", token)

    def test_ttl_must_be_positive(self):
        with self.assertRaises(ValueError):
            self.registry.acquire("gpu-1", "worker-a", 0)
        token = self.registry.acquire("gpu-1", "worker-a", 5)
        with self.assertRaises(ValueError):
            self.registry.renew("gpu-1", "worker-a", token, -1)


if __name__ == "__main__":
    unittest.main()
