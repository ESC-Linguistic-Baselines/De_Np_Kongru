# Standard
import csv
import sys

# Pip
import typer
from tqdm import tqdm

# Custom

# api_general
from kongru.api_general.universal.constants.general_paths import GeneralPaths as Gp
from kongru.api_general.universal.funcs.basic_logger import catch_and_log_error

# api_nlp
from kongru.api_nlp.congruential_analysis.analyzers.demorphy_analyzer import (
    DemorphyAnalyzer,
)
from kongru.api_nlp.congruential_analysis.analyzers.common_entity_recognition import (
    CommonEntityRecognition as Cer,
)


class NominalPhraseCongruency:
    """ """

    def __init__(self, morpho_results, save_file_name=""):
        self.morpho_results = morpho_results
        self.save_file_name = save_file_name

    def prepositional_nominal_phrase(self):
        pass

    def art_def_nominal_phrase(self, extracted_info, sentence, vocabulary, np_demorphy):

        # Nominal
        head = vocabulary[-1]
        res = DemorphyAnalyzer().guess_noun_by_suffix(head)

        (
            _,
            np_genus,
            np_kasus,
            np_numerus,
        ) = extracted_info

        demorphy_check = 0

        for demoprhy_enty in np_demorphy[1][1]:
            demoprhy_enty = demoprhy_enty.replace(" ", ",")
            entry = demoprhy_enty.split(",")

            (
                noun_demorph,
                pos_demorph,
                genus_demorph,
                kasus_demorph,
                numerus_demorph,
            ) = entry
            numerus_demorph = numerus_demorph.replace("plu", "pl")
            numerus_demorph = numerus_demorph.replace("sing", "sg")

            np_morph = (np_genus, np_kasus, np_numerus)
            np_demorph = (genus_demorph, kasus_demorph, numerus_demorph)

            np_morph = [i.lower() for i in np_morph]
            np_demorph = [i.lower() for i in np_demorph]

            demorphy_check = np_morph == np_demorph

            if demorphy_check:
                break

        # Exisitiert das Wort in dem Woerterbuch
        demorphy_dict = DemorphyAnalyzer().get_read_in_demorphy_dict(True)
        word = demorphy_dict.get(res[0])

        if demorphy_check and bool(word) or demorphy_dict and demorphy_dict.get(head):
            return "1"
        else:
            return "0"

    def nominal_phrase_spelling(self, vocabulary_np, demorphy_dict):

        all_words_spelled_correctly = []
        for word in vocabulary_np:
            demorphy_result = demorphy_dict.get(word)
            if demorphy_result is None:
                all_words_spelled_correctly.append(False),
            else:
                all_words_spelled_correctly.append(True)
        return all(all_words_spelled_correctly)

    def nominal_congruency_check(
        self, np_info: dict, np_demorphy: list, demorphy_dict: dict
    ):

        try:
            # Die Informationen aus den entsprechenden Dictionaries extrahieren
            full_np = np_info.get("full_np")
            sentence_np = np_info.get("sentence")
            vocabulary_np = full_np.split(" ")

            # Die morphologischen Information der einzelnen Woertern extrahieren
            vocabulary_morphological_info = list(np_info.values())

            """            
            Die morphologischen Informationen werden aus den jeweilien Nps extrahiert
            und hier gespeichert, damit sie nachher in der Ergebniss-Datei
            gespeichert werden koennen. 
            """
            complete_noun_info = []

            # Hier wird die Np-Analyse-Methoden festgelegt.
            np_type = dict()
            extracted_info = []

            # Rechtschreibung ueberpruefen
            all_words_spelled_correctly = self.nominal_phrase_spelling(
                vocabulary_np, demorphy_dict
            )

            detector = Cer(phrases_or_proper=vocabulary_np)
            np_is_proper_or_common = detector.check_common_phrase_or_proper(
                check_phrase_or_proper_common="proper_common"
            )
            np_is_phrase = detector.check_common_phrase_or_proper(
                check_phrase_or_proper_common="phrase"
            )

            # Die noetigen NP-information extrahieren
            for word_entry in vocabulary_morphological_info:

                # Es gibt einzelne Strings, die ignoriert werden sollen.
                # Deswegen werden nur Dictionaries beruecksichtigtet.
                if isinstance(word_entry, dict):

                    # Die morphologischen Informationen der jeweileigen NPs.
                    noun_info = word_entry.get("noun_info")
                    noun = word_entry.get("noun")
                    pos = word_entry.get("pos")

                    # Die Informationen, die sich in dem NP-Eintrag befinden koennen.
                    word_info = ["def", "genus", "kasus", "numerus"]
                    # Wenn ein Eintrag nicht vorhanden ist, wird es mit "_" bestetzt.
                    extracted_info = [
                        noun_info.get(morpo_info, "_") for morpo_info in word_info
                    ]

                    # Informationen zusammenfuehren und daraus einen String machen
                    combined_extracted_info = "|".join(extracted_info)
                    complete_noun_info.append(
                        " ".join([noun, pos, combined_extracted_info])
                    )

                    # Die Np-Analyse type bestimmen

                    """
                    Wenn die NP nict in dem Satz vorkommt, wird sie nicht beruecksichtigt
                    und gilt automatisch als unbekannt. Eine NP kann z.B. in einem 
                    Satz nicht vorkommen, wenn die Datei nicht korrekt POS-gepaarst.
                    wurde. Es werden auch nicht Nps beruecksichtigt, die 
                    falsch geschrieben wurden. 
                    """
                    if full_np in sentence_np and all_words_spelled_correctly is True:
                        first_word = np_info.get(1).get("pos")
                        # NPs, die mit Artikeln anfangen
                        if first_word == "ART":
                            np_type["TYPE"] = {"ART": True}
                        else:
                            # 99 = NP-Status unbekannt
                            np_type["TYPE"] = "99"

                    # Die NP gilt als falsch, wenn alle Woerter nicht richtig
                    # geschrieben wurden
                    elif all_words_spelled_correctly is False:
                        np_type["TYPE"] = "2"

                    # Eigennamen oder typische Redewendungen werden immer
                    # als wahr gelten
                    elif np_is_proper_or_common or np_is_phrase:
                        np_type["TYPE"] = "1"

            # Die morphologischen Informationen zusammenfuehren
            combined_complete_noun_info = ",".join(complete_noun_info)

            # NP-Typ extrahieren, um die richtige Methoden
            # automatisch bestimmen zu koennen
            congurency_type = np_type.get("TYPE")
            unknown_congruency = ["99", "2"]
            """
            Es wird keine Analyse durchgefuehrt: 
                Moegliche Gruende 
                2 - Wort nicht erkannt auf grund der Rechtschreibung 
                99 - NP ist nicht in dem Satz vorhanden. 
            """

            if congurency_type in unknown_congruency:
                extracted_np_info = [
                    congurency_type,
                    full_np,
                    # morphologische info nach Komma splliten
                    # dann entpacken, damit alles in einer Liste ist.
                    *combined_complete_noun_info.split(","),
                    sentence_np,
                ]

                return extracted_np_info

            # Wenn die NP mit einem Artikel anfaengt.
            if congurency_type.get("ART"):
                congruency_result = self.art_def_nominal_phrase(
                    extracted_info, sentence_np, vocabulary_np, np_demorphy
                )

                # Die NP-Kongruenz-Information
                extracted_np_info = [
                    congruency_result,
                    full_np,
                    # morphologische info nach Komma splliten
                    # dann entpacken, damit alles in einer Liste ist.
                    *combined_complete_noun_info.split(","),
                    sentence_np,
                ]

                return extracted_np_info

            if congurency_type.get("PREP"):
                pass

            if congurency_type.get("COMMON"):
                pass

        except Exception as e:
            catch_and_log_error(error=e, custom_message="___")

    def run_congruency_check(self):
        """ """
        morpho_results = self.morpho_results
        np_data, np_morph = morpho_results.get("np_data"), morpho_results.get(
            "np_morph"
        )

        congruency_results = dict()
        demorphy_dict = DemorphyAnalyzer().get_read_in_demorphy_dict(True)

        for np_key, np_value in tqdm(
            np_data.items(),
            file=sys.stdout,
            disable=True,
            desc="NP-Analyse durchfuehren",
        ):

            np_info = np_data.get(np_key)
            np_demorphy = np_morph.get(np_key)

            if np_info:
                np_analysis = self.nominal_congruency_check(
                    np_info=np_info,
                    np_demorphy=np_demorphy,
                    demorphy_dict=demorphy_dict,
                )
                congruency_results[np_key] = np_analysis

        typer.echo("Np-Analyse abgeschlossen")

        return congruency_results

    def save_congruency_results(self) -> None:
        """
         Die Ergebnisse aus der NP-Analyse speichern.

        Args:
            /

        Returns:
            /
        """

        with open(
            f"{Gp.RES_SAVE_NP.value}_{self.save_file_name}",
            mode="w",
            encoding="utf-8",
        ) as save:
            csv_writer = csv.writer(save, delimiter=",")
            congruency_results = self.run_congruency_check()

            for congruency_entry in congruency_results:
                try:
                    result = congruency_results.get(congruency_entry)
                    csv_writer.writerow(result)

                except Exception as e:
                    catch_and_log_error(
                        error=e,
                        custom_message=f"{congruency_entry} konnte nicht gespeichert werden.",
                    )


if __name__ == "__main__":
    pass
