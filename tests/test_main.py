import unittest


class TestMain(unittest.TestCase):
    def test_runSimple(self):
        self.assertEqual(Hello(), "hello")


if __name__ == "__main__":
    unittest.main()
