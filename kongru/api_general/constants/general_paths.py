# Standard
import os
from enum import Enum

# Pip
# None

# Standard
# None

os.chdir(
    "/Users/christopherchandler/repo/Python/computerlinguistik/NP - Computerlinguistik/DE_np_Kongru"
)


class GeneralPaths(Enum):
    NP_FILE = "user/incoming/np/test_np_file.csv"
    DEMORPHY_DICT = "app_resources/data/morpho_dict/test_DE_morph_dict.txt"
    SAVE_DIRECTORY_NP = "user/outgoing/np_analysis_results"
