# Standard
import os

from enum import Enum

# Pip
# None

# Custom

# Main
from main_config_manager import get_config_data as config

# api_general

# constants
from kongru.api_general.universal.constants.message_keys import MessageKeys
from kongru.api_general.universal.constants.general_vars import SIMPLE_TIMESTAMP

# funcs
from kongru.api_general.universal.funcs.basic_logger import catch_and_log_error


class GeneralPaths(Enum):
    """
    Hier werden alle Pfade als Enum-Werte festgelegt, damit das Programm nachher
    darauf zugreifen kann. Solange das Hauptverzeichnis stimmt,
    kann das Programm auf die unten angegebenen Pfade zugreifen

    Attribute:
        /

    Methoden:
        /

    Beispiel:
         GeneralPaths.DIR_MAIN.value
         # value gibt den String-Wert wieder
    """

    # Verzeichnisse
    DIR_CONLL = None
    DIR_LOG = "app_log"

    # SQL
    SQL_FILE_TYPES = "scripts/file_types.sql"

    # Das muss lokal gesetzt werden.
    # Es haengt von dem jeweiligen Rechner ab.
    DIR_MAIN = config().get("CONFIG_HOME_DIR")

    # Datenbank

    ## Demorphy
    DB_DEMORPHY_TXT = "app_resources/data/demorphy/demorpy_dict.txt"
    DB_DEMORTHY_PKL = "app_resources/data/demorphy/demoprhy_dict.pkl"
    DB_DEMORPHY_TXT_TEST = "app_resources/data/demorphy/test_demorphy_dict.txt"
    DB_DEMORPHY_LEMMA_TXT = "app_resources/data/demorphy/lemmas.txt"

    ## Merlin
    DB_MERLIN_SQL_DB = r"app_resources/data/merlin_corpus/merlin_corpus.db"
    SQL_MERLIN = "scripts/merlin_commands.sql"

    # CER
    CER_PHRASES = "app_resources/data/cer/phrases.txt"
    CER_COMMON_PROPER = "app_resources/data/cer/common_proper.txt"

    # Inflections
    INFLECTION_DEFINITE_YAML = "app_resources/data/inflection/inflection_definite.yaml"
    INFLECTION_INDEFINITE_YAML = (
        "app_resources/data/inflection/inflection_indefinite.yaml"
    )
    INFLECTION_SUFFIXES_YAML = "app_resources/data/inflection/inflection_suffixes.yaml"

    # Ergebnissdateien
    RES_AST_NP_FILE = f"user/outgoing/extracted_nominal_phrases/nps"
    RES_SAVE_NP = f"user/outgoing/nominal_phrase_analysis_results/"

    # Testdateien
    TEST_NP_FILE_CSV = "user/outgoing/extracted_nominal_phrases/nps_1023_0101895.csv"
    TEST_NP_AST_FILE = "1023_0001416.ast"

    # AST DIR
    AST_DIR = "user/incoming/ast"


try:
    """
    Das Hauptverzeichnis soll hier festgelegt werden,
    damit die folgenden Pfade auch nachher stimmen.
    """
    os.chdir(GeneralPaths.DIR_MAIN.value)
except Exception as e:
    catch_and_log_error(
        error=e,
        custom_message=MessageKeys.General.MISSING_HOME_DIR.value,
        kill_if_fatal_error=True,
    )

if __name__ == "__main__":
    pass
