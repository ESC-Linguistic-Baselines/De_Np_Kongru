# Standard
import os

from enum import Enum

# Pip
# None

# Custom

# Main
from main_config_manager import get_config_data as config

## api_general

### funcs
from kongru.api_general.universal.funcs.basic_logger import catch_and_log_error

### constants
from kongru.api_general.universal.constants.message_keys import MessageKeys
from kongru.api_general.universal.constants.general_vars import SIMPLE_TIMESTAMP


class GeneralPaths(Enum):
    """
    Hier werden alle Pfade als Enum-Werte festgelegt, damit das Programm
    nachher darauf zugreifen kann.
    """

    # Verzeichnisse
    DIR_LOG = "app_log"

    # Das muss lokal gesetzt werden.
    # Es haengt von dem jeweiligen Rechner ab.
    DIR_MAIN = config().get("CONFIG_HOME_DIR")

    # Testdateien
    TEST_NP_FILE_CSV = "user/outgoing/np/np_test_1023_0001416.csv"

    # Datenbank

    ## Demorphy
    DB_DEMORPHY_TXT = "app_resources/data/morpho_dict/demorpy_dict.txt"
    DB_DEMORTHY_PKL = "app_resources/data/morpho_dict/demoprhy_dict.pkl"
    DB_DEMORPHY_TXT_TEST = "app_resources/data/morpho_dict/test_demorphy_dict.txt"
    DB_DEMORPHY_LEMMA_TXT = "app_resources/data/morpho_dict/lemmas.txt"

    ## Merlin
    DB_MERLIN_SQL_DB = r"app_resources/data/corpus/merlin_corpus.db"

    # CER
    CER_PHRASES = "app_resources/data/CER/phrases.txt"
    CER_COMMON_PROPER = "app_resources/data/CER/common_proper.txt"

    # Inflections
    INFLECTION_DEFINITE_YAML = "app_resources/data/inflection/inflection_definite.yaml"
    INFLECTION_INDEFINITE_YAML = (
        "app_resources/data/inflection/inflection_indefinite.yaml"
    )
    INFLECTION_SUFFIXES_YAML = "app_resources/data/inflection/inflection_suffixes.yaml"

    # Ergebnissdateien
    RES_AST_NP_FILE = f"user/outgoing/np/nps_{SIMPLE_TIMESTAMP}.csv"
    RES_SAVE_NP = f"user/outgoing/np_analysis_results/{SIMPLE_TIMESTAMP}"


try:
    """
    Das Hauptverzeichnis soll hier festgelegt werden, damit die folgenden Pfade
    auch nachher stimmen.
    """
    os.chdir(GeneralPaths.DIR_MAIN.value)
except Exception as e:
    catch_and_log_error(
        error=e, custom_message=MessageKeys.General.MISSING_HOME_DIR.value
    )
