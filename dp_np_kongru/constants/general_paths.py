# Standard
import os
from enum import Enum

# Pip
# None

# Standard
# None

# Hauptverzeichnis fetlegen
os.chdir(
    "/Users/christopherchandler/repo/Python/computerlinguistik/NP - Computerlinguistik/DE_np_Kongru"
)


class GeneralPaths(Enum):
    NP_FILE = "app_resources/data/np_data/test_np_file.csv"
    DEMORPHY_DICT = (
        "app_resources/data/morph_dict_data/test_DE_morph_dict.txt"
    )
    SAVE_DIRECTORY_NP = "app_resources/results/"
