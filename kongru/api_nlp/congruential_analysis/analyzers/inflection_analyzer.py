# Standard
# None
import yaml

# Pip
# None

# Custom

# universals
from kongru.api_nlp.universal.inflections import Inflections

# constants
from kongru.api_general.universal.constants.general_paths import GeneralPaths as Gp


class InflectionAnalyzer:
    def __init__(
        self,
        article=None,
        adjective=None,
        word=None,
        preposition=None,
        case=None,
        gender=None,
        number=None,
        pos=None,
    ):
        """
        Initialisiert einen InflectionAnalyzer mit verschiedenen Optionen zur Analyse
        von Flexionen.

        Args:
            article (str, optional): Der Artikel der Flexion. Standardwert ist None.
            adjective (str, optional): Das Adjektiv der Flexion. Standardwert ist None.
            word (str, optional): Das zu analysierende Wort. Standardwert ist None.
            preposition (str, optional): Die Präposition der Flexion. Standardwert ist None.
            case (str, optional): Der Kasus der Flexion. Standardwert ist None.
            gender (str, optional): Das Genus (Geschlecht) der Flexion. Standardwert ist None.
            number (str, optional): Die Numerus (Zahl) der Flexion. Standardwert ist None.
            pos (str, optional): Die Wortart (POS) der Flexion. Standardwert ist None.

        """
        # Pfad zur YAML-Datei mit bestimmten Flexionen
        self.inflections_definite = Gp.INFLECTION_DEFINITE_YAML.value

        # Zuweisung der Argumente zu den entsprechenden Attributen
        self.article = article
        self.adjective = adjective
        self.word = word
        self.preposition = preposition
        self.case = case
        self.gender = gender
        self.number = number
        self.pos = pos

    def get_read_in_inflection_files(self):
        """
        Liest die YAML-Datei mit bestimmten Flexionen und gibt ihren Inhalt als
        Python-Datenstruktur zurueck.

        Returns:
            inflection_data(dict): Ein Dictionary, das die Flexionen aus der
            YAML-Datei enthaelt.
        """
        with open(self.inflections_definite, "r") as file:
            inflection_data = yaml.safe_load(file)
            return inflection_data

    def analyze_indefinite_inflections(self, demorphy_dict: dict) -> bool:
        """
        Analysiert die Flexionen für unbestimmte Artikel.

        Args:
            demorphy_dict (dict): Ein Dictionary mit Demorphy-Lexikoneintraegen.

        Returns:
            bool: True, wenn die Flexionen erfolgreich analysiert wurden,
            andernfalls False.
        """

        indefinite_file = self.get_read_in_inflection_files()

        try:
            # Versuchen, die Flexionen aus dem YAML-Dictionary abzurufen
            entry = indefinite_file.get(self.preposition)
            number = entry.get(self.number)
            gender = number.get(self.gender)
            case = gender.get(self.case)

            return True  # Analyse erfolgreich
        except:
            return False  # Analyse fehlgeschlagen


if __name__ == "__main__":
    pass
