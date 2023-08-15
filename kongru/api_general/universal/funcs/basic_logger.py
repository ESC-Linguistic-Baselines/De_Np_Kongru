# Standard
import logging

# Pip
# None

# Custom
from config_parser import get_config_data
from kongru.api_general.universal.constants.general_vars import SIMPLE_TIMESTAMP

"""
Main Body
"""


def get_logger() -> logging.Logger:
    """
    Gibt einen konfigurierten Logger zurück.

    Returns:
        logging.Logger: Ein konfigurierter Logger.
    """
    path_file = get_config_data().get("LOG_PATH")
    logging.basicConfig(
        filename=f"{path_file}/log_{SIMPLE_TIMESTAMP}.log",
        level=logging.ERROR,
        format=(
            "Zeitpunkt: %(asctime)s\n"
            "Loggername: %(name)s\n"
            "LogLevel: %(levelname)s\n"
            "Benutzerdefiniert: %(custom_message)s\n"
            "Nachricht: %(message)s\n"
            "Modul: %(module)s\n"
            "Funktion: %(funcName)s\n"
            "Linie: %(lineno)d\n"
            "Dateipfad: %(pathname)s\n"
        ),
    )

    return logging.getLogger()


if __name__ == "__main__":
    pass
