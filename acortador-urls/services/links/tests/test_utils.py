import unittest

from app.utils import BASE62, is_valid_alias, random_code


class TestUtils(unittest.TestCase):
    def test_random_code_length_and_alphabet(self):
        code = random_code()
        self.assertEqual(len(code), 7)
        self.assertTrue(all(c in BASE62 for c in code))

    def test_random_code_is_not_constant(self):
        self.assertGreater(len({random_code() for _ in range(200)}), 190)

    def test_valid_aliases(self):
        for alias in ("abc", "mi-enlace_1", "A" * 32):
            self.assertTrue(is_valid_alias(alias), alias)

    def test_invalid_aliases(self):
        for alias in ("ab", "A" * 33, "con espacio", "ñandú", "a/b", "api", "APP", "Docs", ""):
            self.assertFalse(is_valid_alias(alias), alias)


if __name__ == "__main__":
    unittest.main()
