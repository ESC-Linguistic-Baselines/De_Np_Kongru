# Standard
import os
from enum import Enum
import inspect

# Pip
# None

# Standard
from config_parser import get_config_data
from kongru.api_general.universal_functions.basic_logger import get_logger
from kongru.api_general.constants.message_keys import MessageKeys


try:
    """
    Das Hauptverzeichnis soll hier festgelegt werden, damit die folgenden Pfade
    auch nachher stimmen.
    """
    os.chdir(get_config_data().get("HOME"))
except Exception as e:
    logger = get_logger()
    logger.error(e)
    raise SystemExit(MessageKeys.General.MISSING_HOME_DIR.value)


class GeneralPaths(Enum):
    """
    Hier werden alle Pfade als Enum-Werte festgelegt, damit das Programm
    nachher darauf zugreifen kann.
    """

    NP_FILE = "user/incoming/np/test_np_file.csv"
    DEMORPHY_DICT = "app_resources/data/morpho_dict/test_DE_morph_dict.txt"
    SAVE_DIRECTORY_NP = "user/outgoing/np_analysis_results"
