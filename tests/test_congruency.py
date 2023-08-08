import unittest
from dp_np_kongru.annotator_analyzers.congruency_analyzer import quick_analysis


def Hello():
    return "hello"


class TestCongruency(unittest.TestCase):
    def test_main(self):
        self.assertEqual(quick_analysis.run_quick_analysis(), True)


if __name__ == "__main__":
    unittest.main()
