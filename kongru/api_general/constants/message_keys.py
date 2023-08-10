# Standard
from enum import Enum

# Pip
# None

# Standard
# None


class MessageKeys:
    class Merlin(Enum):

        # Info
        INFO_TEXT_OR_META = "Entweder 'text' oder 'meta' als Wert angeben"

        # Fehler
        ERR_MISSING_SEPARATOR = "Das Standardtrennzeichen fehlt in der Datei."
