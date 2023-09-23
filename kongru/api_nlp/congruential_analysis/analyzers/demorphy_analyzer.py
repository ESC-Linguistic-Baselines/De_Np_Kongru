# Standard
# None


# Pip
# None

# Custom

# general
from kongru.api_general.database_managers.managers.demorphy_manager import (
    DemorphyManager,
)
from kongru.api_nlp.congruential_analysis.analyzers.inflection_analyzer import (
    InflectionAnalyzer,
)

# nlp
from kongru.api_nlp.congruential_analysis.analyzers.suffix_analyzer import (
    SuffixAnalyzer,
)
from kongru.api_nlp.congruential_analysis.analyzers.token_analyzer import TokenAnalyzer


class DemorphyAnalyzer(
    DemorphyManager, SuffixAnalyzer, TokenAnalyzer, InflectionAnalyzer
):
    """
    Eine Klasse zur Analyse und Verarbeitung von Textdaten mithilfe von Demorphy und
    verschiedenen Analysatoren.
    Diese Klasse erbt von mehreren anderen Klassen, um eine Vielzahl von Analysefunktionen
    bereitzustellen.
    Sie kombiniert alle Klassen zusammen, damit nur diese Klasse aufgerufen werden muss.
    Die Argumente werden auch weiter gegeben

    Args:
        DemorphyManager (class): Eine Managerklasse für Demorphy-Daten und Ressourcen.
            - Demorphy Dateien einlesen
        SuffixAnalyzer (class): Ein Analysator fuer Suffixe in Textdaten.
            - Suffixe von Tokens bestimmen
        TokenAnalyzer (class): Ein Analysator für Token   in Textdaten.
            - Tokenart bestimmen
        InflectionAnalyzer (class): Ein Analysator für Flexionen in Textdaten.
            - Die Inflektion in Tokens bestimmen
    """

    def __init__(
        self,
        article=None,
        adjective=None,
        word=None,
        file_name=None,
        sentence=None,
        token=None,
        preposition=None,
        case=None,
        number=None,
        pos=None,
        gender=None,
    ):
        self.article = article
        self.adjective = adjective
        self.word = word
        self.file_name = file_name
        self.sentence = sentence
        self.token = token
        self.case = case
        self.gender = gender
        self.number = number
        self.pos = pos

        # die verschiedenen Konstruktoren aufrufen und die Parameter weitergeben
        # damit nur diese Klasse aufgerufen werden muss.
        DemorphyManager.__init__(self, file_name)
        SuffixAnalyzer.__init__(self, word)
        TokenAnalyzer.__init__(self, sentence, token)
        InflectionAnalyzer.__init__(
            self, article, adjective, word, preposition, case, gender, number, pos
        )

    def get_raw_np_morphology(self) -> dict:
        """
        Diese Methode extrahiert die Rohmorphologie von Nominalphrasen (NPs)
        aus den gelesenen Daten.

        Sie verwendet die zuvor geladenen NP-Daten und Demorphy-Lexikoneinträge,
        um die Morphologie
        für jede NP im Dictionary zu erfassen.

        Returns:
            np_morh_results(dict): Ein dict, das die extrahierte Morphologie der NPs
            und die ursprünglichen NP-Daten enthaelt.

        Beispiel:
            Die Ausgabe kann wie folgt aussehen:

            {
                "np_data": {
                    '1_Katharina': {'full_np': 'Katharina', 'sentence':
                    'Katharina .', 1: {...}},
                    # Weitere NP-Daten fuer andere NPs...
                },
                "np_morph": {
                    '1_Katharina': [
                        ('Katharina', ['Katharina NN,fem,dat,sing',
                        'Katharina NN,fem,nom,sing', ...]),
                        # Weitere Morphologiedaten für andere NPs...
                    ],
                    # Weitere NP-Morphologie für andere NPs...
                }
            }
        """
        np_morph = dict()  # Ein leeres Dictionary zur Speicherung der NP-Morphologie
        np_data = self.get_read_in_np_file()  # Holen der geladenen NP-Daten

        morph_dict = self.get_read_in_demorphy_dict()  # Holen der Demorphy-
        # Lexikoneintraege

        # Schleife durch die NP-Daten
        for key in np_data:
            full_np = np_data.get(key).get("full_np")
            tokens = full_np.split(" ")  # Aufteilen der NP in einzelne Tokens

            np_morph[key] = list()  # Ein leeres Listenelement für die aktuelle NP

            # Schleife durch die Tokens in der NP
            for t in tokens:
                # Hinzufügen des Token und der zugehörigen Demorphy-Morphologiedaten
                # zur Liste
                np_morph[key].append((t, morph_dict.get(t)))

        # Zusammenführen der NP-Daten und der extrahierten NP-Morphologie
        # in einem Ergebnis-Dictionary
        np_morh_results = {"np_data": np_data, "np_morph": np_morph}

        return np_morh_results


if __name__ == "__main__":
    pass
