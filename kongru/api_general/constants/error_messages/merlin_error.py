# Standard

# Pip
# None

# Custom
from kongru.api_general.constants.message_keys import MessageKeys as Mk


class MerlinError:
    class MissingSeparator(Exception):
        """
        Wenn das Standard Leerzeichen in der Merlin-Datei fehlt,
        kann die Datei nicht wie vorgesehen gepaarst werden.
        """

        def __init__(self):
            message = Mk.Merlin.ERR_MISSING_SEPARATOR.value
            super().__init__(message)
