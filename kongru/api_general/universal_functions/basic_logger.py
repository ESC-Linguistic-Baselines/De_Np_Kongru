# Standard
import logging

# Pip
# None

# Custom
from config_parser import get_config_data
from kongru.api_general.constants.general_vars import SIMPLE_TIMESTAMP

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
        format="Zeitpunkt: %(asctime)s\nModul: %(module)s\nLogLevel: %(levelname)s\nNachricht: %(message)s\nLinie: %(lineno)d\n\n",
    )
    return logging.getLogger()


if __name__ == "__main__":
    pass
