class MerlinError:
    class MissingSeparator(Exception):
        """
        Wenn das Standard Leerzeichen in der Merlin-Datei fehlt,
        kann die Datei nicht wie vorgesehen gepaarst werden.
        """
        def __init__(self):
            message = "Das Standardtrennzeichen fehlt in der Datei."
            super().__init__(message)




