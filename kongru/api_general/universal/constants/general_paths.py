# Standard
import os
from enum import Enum

# Pip
# None

# Standard
from config_parser import get_config_data
from kongru.api_general.universal.funcs.basic_logger import get_logger
from kongru.api_general.universal.constants.message_keys import MessageKeys


class GeneralPaths(Enum):
    """
    Hier werden alle Pfade als Enum-Werte festgelegt, damit das Programm
    nachher darauf zugreifen kann.
    """
    MAIN_DIR = get_config_data().get("HOME")
    NP_FILE = "user/incoming/np/test_np_file.csv"
    DEMORPHY_DICT = "app_resources/data/morpho_dict/test_DE_morph_dict.txt"
    SAVE_DIRECTORY_NP = "user/outgoing/np_analysis_results"
    MERLIN_DB = r"app_resources/data/corpus/merlin_corpus.db"
    LOG_PATH = "app_log"


try:
    """
    Das Hauptverzeichnis soll hier festgelegt werden, damit die folgenden Pfade
    auch nachher stimmen.
    """
    os.chdir(GeneralPaths.MAIN_DIR.value)
except Exception as e:
    logger = get_logger()
    logger.error(e)
    raise SystemExit(MessageKeys.General.MISSING_HOME_DIR.value)

