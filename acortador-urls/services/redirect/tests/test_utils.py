import unittest

from app.utils import CODE_RE, TTLCache, hash_ip


class FakeClock:
    def __init__(self):
        self.now = 0.0

    def __call__(self):
        return self.now


class TestTTLCache(unittest.TestCase):
    def test_get_set_and_expiry(self):
        clock = FakeClock()
        cache = TTLCache(ttl=10, clock=clock)
        cache.set("a", 1)
        self.assertEqual(cache.get("a"), 1)
        clock.now = 9.9
        self.assertEqual(cache.get("a"), 1)
        clock.now = 10.1
        self.assertIsNone(cache.get("a"))

    def test_missing_key(self):
        self.assertIsNone(TTLCache().get("nope"))

    def test_max_items_clears(self):
        cache = TTLCache(ttl=10, max_items=2, clock=FakeClock())
        cache.set("a", 1)
        cache.set("b", 2)
        cache.set("c", 3)  # lleno: se vacía y se inserta
        self.assertIsNone(cache.get("a"))
        self.assertEqual(cache.get("c"), 3)


class TestHelpers(unittest.TestCase):
    def test_code_regex(self):
        self.assertTrue(CODE_RE.match("aB3_-9x"))
        self.assertFalse(CODE_RE.match("ab"))
        self.assertFalse(CODE_RE.match("../etc"))

    def test_hash_ip_is_stable_and_short(self):
        self.assertEqual(hash_ip("1.2.3.4", "s"), hash_ip("1.2.3.4", "s"))
        self.assertNotEqual(hash_ip("1.2.3.4", "s"), hash_ip("1.2.3.5", "s"))
        self.assertEqual(len(hash_ip("1.2.3.4", "s")), 16)


if __name__ == "__main__":
    unittest.main()
