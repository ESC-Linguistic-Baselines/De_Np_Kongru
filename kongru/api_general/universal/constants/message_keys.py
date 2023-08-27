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

    class Merlin(Enum):
        # Fehler
        ERR_MISSING_SEPARATOR = "Das Standardtrennzeichen fehlt in der Datei."

    class General(Enum):
        # Fehler
        MISSING_HOME_DIR = "Das Hauptverzeichnis wurde nicht richtig angegeben."

    class CER(Enum):
        # Fehler
        INCORRECT_ARGUMENT = (
            "Entweder 'phrases' oder 'proper_common' als Argument angeben."
        )
