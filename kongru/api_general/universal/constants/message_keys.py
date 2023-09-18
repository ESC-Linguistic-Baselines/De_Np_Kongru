# Standard
from enum import Enum


# Pip
# None

# Standard
# None


class MessageKeys:
    """
    Hier werden die Nachrichten und Meldungen, die vom Programm ausgegeben,
    zentral gespeichert.
    """

    class General(Enum):
        # Fehler
        MISSING_HOME_DIR = "Das Hauptverzeichnis wurde nicht richtig angegeben."
        FILE_TYPE_LONG = "--datei_type"
        FILE_TYPE_SHORT = "--datei"
        FILE_MISSING = "Die Datei ist nicht vorhanden"

    class MainApp(Enum):
        APP_NAME_HELP = "Die HauptApp "
        EMPTY_DIRECTORY_HELP = "verzeichnis_leeren"
        EMPTY_DIRECTORY = "Ein ausgewaehltes Verzeichnis leeren"
        APP_NAME = "DE_Np_Kongru"

        EMPTY_DIRECTORY_TRG_LONG = "--trg_dir"
        EMPTY_DIRECTORY_TRG_SHORT = "--trg"
        EMPTY_DIRECTORY_TRG_HELP = "Das Verzeichnis, das geleert werden soll."

        FILE_TYPE_DEFAULT = "log"
        FILE_TYPE_HELP = "Die Dateien, die geloescht werden sollen."

        help = ("Die Dateien, die geloescht werden sollen.",)
        MAIN_APP_FATAL_ERROR = (
            "Ein Problem ist innerhalb der Hauptanwendung aufgetreten. "
            "Bitte die Protokolldatei für weitere Informationen überprüfen. "
        )
        MAIN_APP_START = "Die Hauptanwendung wurde gestartet."

    class Merlin(Enum):
        # Fehler
        ERR_MISSING_SEPARATOR = "Das Standardtrennzeichen fehlt in der Datei."
        INVALID_TEXT_ID = "Die Text-ID, die eingegeben wurde, ist nicht gueltig."
        TEXT_IDS_PROCESS = "Text Ids verarbeiten"

        MERLIN_DATABASE_READ_ERR = (
            "Beim auslesen der Datenbank ist ein Fehler " "aufgetreten. "
        )

        MERLIN_DATABASE_UNZIP_DATA = "Der Merlin-Korpus fehlt. Ohne das Zip-Verchnis kann keine Datenbank erstellt werden."

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

        GET_AND_SHOW_TEXT_BY_ID_COMMAND_NAME = "text_lesen"
        GET_AND_SHOW_TEXT_BY_ID_COMMAND_HELP = (
            "einen bestimmten Text in der Datenbank lesen"
        )
        GET_AND_SHOW_TEXT_BY_ID_TEXT_ID_DEFAULT = "1031_0003130"
        GET_AND_SHOW_TEXT_BY_ID_TEXT_ID_LONG = "--text_id"
        GET_AND_SHOW_TEXT_BY_ID_TEXT_ID_SHORT = "--id"
        GET_AND_SHOW_TEXT_BY_ID_TEXT_ID_HELP = (
            "Die Text-Id des gewuenschten Textes angeben"
        )
        GET_AND_SHOW_TEXT_BY_ID_VARIABLE_NAME = ""
        GET_AND_SHOW_TEXT_BY_ID_MERLIN_TXT_ID = ""
        GET_AND_SHOW_TEXT_BY_ID_CUSTOM_MESSAGE = ""

    class Statistics(Enum):
        APP_NAME = "statistik"
        DEKONGRU_ACCURACY_NAME = "Performanz"
        DEKONGRU_ACCURACY_NAME_HELP = "Die Performanz des Programms anzeigen"

    class NominalPhraseCongruency(Enum):
        pass

    class CER(Enum):
        # Fehler
        INCORRECT_ARGUMENT = (
            "Entweder 'common_phrases' oder 'proper_common' als Argument angeben."
        )
