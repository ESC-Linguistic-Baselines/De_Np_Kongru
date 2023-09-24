# Standard
# None

# Pip
import textdistance as td

# Custom

# constants
from kongru.api_general.universal.constants.general_paths import GeneralPaths as Gp

# error messages
from kongru.api_general.universal.constants.custom_error_messages import (
    CustomErrorMessages as CusEm,
)


class CommonEntityRecognizer:
    """
    Common Entity Recognizer ist eine Klasse zur Identifizierung von haeufigen Phrasen
    oder Eigennamen, indem ihre aehnlichkeit mit einer vordefinierten Liste von haeufigen
    Phrasen oder  Eigennamen berechnet wird.
    """

    def __init__(
        self,
        phrases_or_proper: list = None,
        common_threshold=80,
    ):
        self.common_phrases: str = Gp.CER_COMMON_PHRASES.value
        self.common_proper: str = Gp.CER_COMMON_PROPER.value
        self.phrases_or_proper_common: list = phrases_or_proper
        self.common_threshold: int = common_threshold

    def __load_in_ner_data(self):
        """
        Laedt die Daten fuer das Named Entity Recognition (NER).

        Die Methode oeffnet die Dateien mit haeufigen Phrasen und Eigennamen und
         liest sie ein.

        Returns:
            common_results(dict): Ein dict mit den geladenen Daten, bestehend aus:
                - "common_phrases": Eine Liste von haeufigen Phrasen.
                - "common_proper": Eine Liste von haeufigen Eigennamen.
        """
        common_phrases = open(
            self.common_phrases, mode="r", encoding="utf-8"
        ).readlines()
        common_proper = open(self.common_proper, mode="r", encoding="utf-8").readlines()
        common_results = {
            "common_phrases": common_phrases,
            "common_proper": common_proper,
        }

        return common_results

    def check_common_phrase_or_proper(self, entity_check="common_phrases"):
        """
        ueberprueft die aehnlichkeit zwischen den eingegebenen Phrasen oder Eigennamen
        und den geladenen Daten
        fuer haeufige Phrasen oder Eigennamen.

        Args:
            entity_check (str, optional): Die Art der zu ueberpruefenden Entitaet.
            Kann "phrase" fuer Phrasen
                oder "proper_common" fuer haeufige Eigennamen sein. Standardmaessig ist
                 es "phrase".

        Returns:
            dict or list: Ein dict mit uebereinstimmenden Eintraegen und ihren
            aehnlichkeitspunkten, wenn uebereinstimmungen gefunden wurden.
            Andernfalls wird eine leere Liste zurueckgegeben.
        Raises:
            CusEm.CerPhraseorProperArgument: Wenn `entity_check` einen ungueltigen
            Wert hat.
        """

        common_phrases = self.__load_in_ner_data().get("common_phrases")
        common_proper = self.__load_in_ner_data().get("common_proper")

        similarity_results = {}

        if entity_check == "common_phrases":
            checklist = common_phrases
        elif entity_check == "common_proper":
            checklist = common_proper
        else:
            raise CusEm.CerPhraseorProperArgument

        for reference_entry in checklist:
            for word in self.phrases_or_proper_common:
                reference_entry = reference_entry.strip().lower()
                word = word.strip().lower()
                td_results = round(td.cosine(reference_entry, word) * 100, 2)
                if td_results > self.common_threshold:
                    similarity_results[word] = {
                        "reference_entry": reference_entry,
                        "similarity": td_results,
                    }
        if similarity_results:
            return similarity_results
        else:
            return []


if __name__ == "__main__":
    pass
