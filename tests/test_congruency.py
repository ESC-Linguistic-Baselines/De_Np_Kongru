import unittest


def Hello():
    return "hello"


class TestCongruency(unittest.TestCase):
    def test_runSimple(self):
        self.assertEqual(Hello(), "hello")


if __name__ == "__main__":
    unittest.main()
