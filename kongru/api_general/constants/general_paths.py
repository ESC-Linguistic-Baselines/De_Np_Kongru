# Standard
import os
from enum import Enum

# Pip
# None

# Standard
from kongru.api_general.universal_functions.config_parser import get_config_data

os.chdir(get_config_data().get("HOME"))


class GeneralPaths(Enum):
    NP_FILE = "user/incoming/np/test_np_file.csv"
    DEMORPHY_DICT = "app_resources/data/morpho_dict/test_DE_morph_dict.txt"
    SAVE_DIRECTORY_NP = "user/outgoing/np_analysis_results"
