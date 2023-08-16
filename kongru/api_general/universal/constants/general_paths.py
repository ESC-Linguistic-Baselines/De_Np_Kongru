# Standard
import os
from enum import Enum

# Pip
# None

# Standard
from kongru.api_general.universal.funcs.basic_logger import get_logger
from kongru.api_general.universal.constants.message_keys import MessageKeys
from kongru.api_general.universal.constants.general_vars import SIMPLE_TIMESTAMP


class GeneralPaths(Enum):
    """
    Hier werden alle Pfade als Enum-Werte festgelegt, damit das Programm
    nachher darauf zugreifen kann.
    """

    # Verzeichnisse
    DIR_LOG = "app_log"
    DIR_MAIN = (
        "/Users/christopherchandler/repo/Python/computerlinguistik/NP "
        "- Computerlinguistik/DE_np_Kongru"
    )

    # Testdateien
    TEST_NP_FILE = "user/outgoing/np/test_np_file.csv"

    # Datenbank
    DB_DEMORPHY_TXT = "app_resources/data/morpho_dict/demorpy_dict.txt"
    DB_MERLIN_SQL_DB = r"app_resources/data/corpus/merlin_corpus.db"

    # Ergebnissdateien
    RES_AST_NP_FILE = f"user/outgoing/np/nps_{SIMPLE_TIMESTAMP}.csv"
    RES_SAVE_NP = (
        f"user/outgoing/np_analysis_results/quick_results_{SIMPLE_TIMESTAMP}.csv"
    )


try:
    """
    Das Hauptverzeichnis soll hier festgelegt werden, damit die folgenden Pfade
    auch nachher stimmen.
    """
    os.chdir(GeneralPaths.DIR_MAIN.value)
except Exception as e:
    logger = get_logger()
    logger.error(e)
    raise SystemExit(MessageKeys.General.MISSING_HOME_DIR.value)
