import unittest

from kongru.api_general.universal_functions import read_in_np_file


class TestRaders(unittest.TestCase):
    def test_runNPReader(self):
        f = (
            r"/Users/christopherchandler/repo/Python/small_projects/"
            r"De_NP_Kongru/dp_np_kongru/app_resources/data/np_data/np_file.csv"
        )
        results = read_in_np_file(file_name=f)
        data = {
            "1_den kleinen Hund": (
                "den kleinen Hund",
                [" den DET", " kleinen ADJ", " Hund NN", " acc"],
            )
        }
        self.assertEqual(results, data)


if __name__ == "__main__":
    unittest.main()
