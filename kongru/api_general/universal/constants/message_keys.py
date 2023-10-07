# Standard
from enum import Enum

# Pip
# None

# Standard
# None


class MessageKeys:
    """
    Hier werden die Bezeichnungen und Meldungen, die vom Programm ausgegeben,
    zentral gespeichert.
    """

    class General(Enum):

        FILE_TYPE_LOG = "log"
        FILE_NAME_LONG = "--datei_name"
        FILE_NAME_SHORT = "--name"
        FILE_NAME_HELP = "Der Name der Datei, die ausgewertet werden soll."

        FILE_TYPE_LONG = "--datei_typ"
        FILE_TYPE_SHORT = "--typ"

        SAVE_DIR_LONG = "--speichern-verzeichnis"

        SAVE_DEFAULT_CSV = "np.csv"
        SAVE_RESULTS_LONG = "--speichern-ergebnisse"
        SAVE_DIR_SHORT = "--speichern"
        SAVE_RESULTS_HELP = "Der Name des Ergebnisdatei"

        SAVE_DIR_HELP = "Das Verzeichnis, worin die Ergebnisse gespeichert werden."

        # Fehler
        MISSING_HOME_DIR = "Das Hauptverzeichnis wurde nicht richtig angegeben."
        GENERAL_ERROR = "Ein Fehler ist aufgetreten."
        FILE_MISSING = "Die Datei ist nicht vorhanden."

    class MainApp(Enum):
        APP_NAME = "de_np_kongru"
        APP_NAME_HELP = "Die Hauptapp von DeNpKongru"

        EMPTY_DIRECTORY = "Ein ausgewaehltes Verzeichnis leeren"
        EMPTY_DIRECTORY_HELP = "verzeichnis_leeren"

        EMPTY_DIRECTORY_TRG_LONG = "--trg_dir"
        EMPTY_DIRECTORY_TRG_SHORT = "--trg"
        EMPTY_DIRECTORY_TRG_HELP = "Das Verzeichnis, das geleert werden soll."

        EMPTY_BULK_DIRECTIORIES_NAME = "kongruenz_leeren"
        EMPTY_BULK_DIRECTIORIES_HELP = "Verzeichnisse der Kongruenz-Ergebnisse leeren"

        FILE_TYPE_HELP = (
            "Die Dateien, die geloescht werden sollen. 'alle' loescht "
            "\nalle Dateien im angegebenen Verzeichnis "
        )

        MAIN_APP_START = "Die Hauptanwendung wurde gestartet."
        MAIN_APP_FATAL_ERROR = (
            "Ein Problem ist innerhalb der Hauptanwendung aufgetreten. "
            "Bitte die Log-Datei überprüfen. "
        )

    class Merlin(Enum):
        # Fehler
        ERR_MISSING_SEPARATOR = "Das Standardtrennzeichen fehlt in der Datei."
        INVALID_TEXT_ID = "Die Text-Id, die eingegeben wurde, ist nicht gueltig."
        TEXT_IDS_PROCESS = "Die Text-Ids verarbeiten"

        MERLIN_DATABASE_READ_ERR = (
            "Beim auslesen der Datenbank ist ein Fehler aufgetreten. "
        )
        MERLIN_DATABASE_UNZIP_DATA = (
            "Der Merlin-Korpus fehlt. Ohne das Zip-Verchnis "
            "kann keine Datenbank erstellt werden."
        )

        MERLIN_DELETE_SQL_INVALID = "'DELETE' darf nicht im SQL-Befehl sein."

    class AppDataManager(Enum):
        APP_NAME = "datenbank"
        APP_NAME_HELP = "Die Datenbankcorpora verwalten und durchsuchen"

        SHOW_TEXT_IDS_COMMAND_NAME = "text_ids"
        SHOW_TEXT_IDS_COMMAND_HELP = "Ids der Textdateien auflisten"

        SHOW_TEXT_IDS_SQL_COMMAND = (
            "SELECT general_author_id,general_mother_tongue,general_cefr,"
            "txt_len_in_char FROM learner_text_data "
        )

        SHOW_TEXT_IDS_COLUMN_NAMES = (
            "general_author_id",
            "general_mother_tongue",
            "general_cefr",
            "txt_len_in_char",
        )

        GET_AND_SHOW_TEXT_BY_ID_NAME = "text_lesen"
        GET_AND_SHOW_TEXT_BY_ID_HELP = "einen bestimmten Text in der Datenbank lesen"
        GET_AND_SHOW_TEXT_BY_ID_TEXT_ID_DEFAULT = "1031_0003130"
        GET_AND_SHOW_TEXT_BY_ID_TEXT_ID_LONG = "--text_id"
        GET_AND_SHOW_TEXT_BY_ID_TEXT_ID_SHORT = "--id"
        GET_AND_SHOW_TEXT_BY_ID_TEXT_ID_HELP = (
            "Die Text-Id des gewuenschten Textes angeben"
        )

        EXTRACT_NPS_FROM_DATABASE_NAME = "nps_datenbank"
        EXTRACT_NPS_FROM_DATABASE_HELP = (
            "Nps aus einem bestimmen Datenbankeintrag extrahieren"
        )
        EXTRACT_NPS_FROM_DATABASE_DATA_DEFAULT = "ast_nps"

        EXTRACT_NPS_FROM_DATABASE_DATA_HELP = (
            "'ast_nps' oder 'conll' als argument angeben"
        )

        EXTRACT_NPS_FROM_DATABASE_TEXT_DEFAULT = "1023_0001416"
        EXTRACT_NPS_FROM_DATABASE_TEXT_LONG = "--text_id"
        EXTRACT_NPS_FROM_DATABASE_TEXT_SHORT = "--id"
        EXTRACT_NPS_FROM_DATABASE_TEXT_HELP = (
            "Die Text-Id des gewuenschten Textes angeben"
        )
        EXTRACT_INCORRECT_ERR = "Die Eingabe war falsch."
        EXTRACT_SAVE_NPS = "Die Ast-Datei wurde ausgelesen und gespeichert."

        EXTRACT_NPS_LOCAL_NAME = "nps_datei"
        EXTRACT_NPS_LOCAL_HELP = "Nps aus einer bestimmen Datei extrahieren"

        EXTRACT_NPS_LOCAL_FILE_DEFAULT = "ast_nps"

        EXTRACT_NPS_LOCAL_FILE_HELP = "'ast_nps' oder 'conll' als argument angeben"

        EXTRACT_NPS_LOCAL_ECHO_DEFAULT = True
        EXTRACT_NPS_LOCAL_ECHO = "--echo"
        EXTRACT_NPS_LOCAL_MUTE = "--mute"
        EXTRACT_NPS_LOCAL_ECHO_HELP = "Die Fortschittsdaten in der Konsole anzeigen"

        EXTRACT_NPS_LOCAL_ECHO_SAVE = "Die Ast-Datei wurde ausgelesen und gespeichert."

        EXTRACT_DATA_FROM_MERLIN_NAME = "daten_extrahieren"
        EXTRACT_DATA_FROM_MERLIN_HELP = "Die Befehle ausfuehren aus der SQL-Datei"

        EXTRACT_DATA_FROM_MERLIN_SQL_LONG = "--sql_script"
        EXTRACT_DATA_FROM_MERLIN_SQL_SHORT = "--sql"
        EXTRACT_DATA_FROM_MERLIN_SQL_HELP = "Der Name der SQL-Datei"

        EXTRACT_DATA_FROM_MERLIN_EXT_DEFAULT = "ast"
        EXTRACT_DATA_FROM_MERLIN_EXT_LONG = "--datei_endung"
        EXTRACT_DATA_FROM_MERLIN_EXT_SHORT = "--endung"
        EXTRACT_DATA_FROM_MERLIN_EXT_HELP = "Die Dateiendung festlegen"

        EXTRACT_AST_DATA_DSC = "Ast-Dateien extrahieren"

    class Statistics(Enum):
        APP_NAME = "statistik"
        APP_NAME_HELP = "Eine einfache Analyse ueber DeNpKongru ausfuehren"

        DEKONGRU_ACCURACY_NAME = "performanz"
        DEKONGRU_ACCURACY_NAME_HELP = "Die Performanz des Programms anzeigen"

        GOLD_AND_RAW_FILES_INCORRECT = (
            "Die Auswertung des Programms konnte nicht "
            "erfolgreich durchgefuehrt werden.\nVermutlich "
            "stimmen die Anzahl der Gold- und Rohdateien "
            "nicht miteinander ueberein.\nDie Anzahl der "
            "Dateien muss ggf. korrigiert werden. "
        )

    class AppCongruentialAnalysis(Enum):
        APP_NAME = "kongruenz"
        APP_NAME_HELP = "Die Np-Eintraege auswerten"

        NP_AGREEMENT_SAVE = "Die Ergebnisse der Auswertung wurden gespeichert."
        NP_AGREEMENT_ERR = "Bei der Analyse ist etwas schief gelaufen."

        NP_AGREEMENT_SINGULAR_NAME = "singular"
        NP_AGREEMENT_SINGULAR_HELP = "Die Kongruenz der Nps in einer Datei bestimmen"

        NP_AGREEMENT_MULTI_NAME = "multi"
        NP_AGREEMENT_MULTI_HELP = "Die Kongruenz der Nps in mehreren Dateien bestimmen"

        MULTI_AGREEMENT_AMOUNT_DEFAULT = 5
        MULTI_AGREEMENT_AMOUNT_LONG = "--text_anzahl"
        MULTI_AGREEMENT_AMOUNT_SHORT = "--anzahl"
        MULTI_AGREEMENT_AMOUNT_HELP = (
            "bestimmt wie viele Texte verarbeitet werden " "sollen "
        )
        MULTI_AGREEMENT_AMOUNT_SAVE_FALSE = "--kongruenz"
        MULTI_AGREEMENT_AMOUNT_SAVE_HELP = (
            "Multi-kongruenz durchfuehren oder Ergebnisse speichern"
        )
        MULTI_AGREEMENT_ID_SOURCE_DEFAULT = 5
        MULTI_AGREEMENT_ID_SOURCE_LONG = "--text_id_quelle"
        MULTI_AGREEMENT_ID_SOURCE_SHORT = "--quelle"
        MULTI_AGREEMENT_ID_SOURCE_HELP = (
            "bestimmt aus welcher Datei, die Ids gelesen " "werden sollen."
        )

        NP_AGEREMENT_SAVE_DEFAULT = False
        NP_AGREEMENT_SAVE_TRUE = "--speichern"
        NP_AGREEMENT_SAVE_FALSE = "--anzeigen"
        NP_AGREEMENT_SAVE_HELP = "Ergebnisse speichern oder anzeigen"

        GENERATE_JSON_FILES = ".json Dateien generieren"
        JSON_CSV_CREATED_COM = ".json und .csv Ergebnisse zusammenfuehren"

        JSON_CSV_CREATED_COM_SUCCESS = (
            ".json und .csv Ergebnisse erfolgreich zusammengefuehrt worden."
        )

        AST_DATA_EXTRACTED = "AST-Dateien erfolgreich extrahiert!"
        NP_DATA_EXTRACT = "Nominalphrasen aus AST-Dateien extrahieren"
        NP_DATA_EXTRACTED = "Nominalphrasen erfolgreich extrahiert!"
        NP_COUNT_RESULTS = "die Ergebnisse aus der NP-Datei zaehlen."
        NP_RESULTS_COUNTED = "Ergebnisse erfolgreich gezaehlt!"
        GENERATE_RESULT_FILES = "Ergebnisdatei generieren"
        RESULT_FILES_CREATED = "Ergebnisdatei erfolgreich generiert!"

    class NominalPhraseCongruency(Enum):
        NP_ART_ERR = "Np konnte als ART nicht verarbeitet werden."
        MISSING_KEY = "Key in dem 'token_data' ist nicht vorhanden"
        PREP_ERR = (
            "Die Bestimmung ueberber Praeposition konnte nicht durchgefuehrt werden.",
        )
        ANALYSIS_FAILED = "Die Analyse konnte nicht erfolgreich durchgefuehrt werden."

    class CER(Enum):
        # Fehler
        INCORRECT_ARGUMENT = (
            "Entweder 'common_phrases' oder 'proper_common' als Argument angeben."
        )
