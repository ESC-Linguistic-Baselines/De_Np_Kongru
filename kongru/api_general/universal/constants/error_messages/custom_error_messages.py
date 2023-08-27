# Standard
# None

# Pip
# None

# Custom
from kongru.api_general.universal.constants.message_keys import MessageKeys as Mk


class CustomErrorMessages:
    """
    Hier werden Fehler angegeben, die bei gewissen Funktionen auftauchen koennten
    """

    class MerlinMissingSeparator(Exception):
        """
        Wenn das Standard Leerzeichen in der Merlin-Datei fehlt,
        kann die Datei nicht wie vorgesehen gepaarst werden.
        """

        def __init__(self):
            message = Mk.Merlin.ERR_MISSING_SEPARATOR.value
            super().__init__(message)

    class CerPhraseorProperArgument(Exception):
        def __init__(self):
            message = "Entweder 'phrases' oder 'proper_common' als Argument angeben."
            super().__init__(message)
