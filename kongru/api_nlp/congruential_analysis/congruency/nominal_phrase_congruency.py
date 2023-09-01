# Standard
import copy
import csv
import sys

# Pip
import typer
from tqdm import tqdm

# Custom

# api_general

# universals
from kongru.api_general.universal.constants.general_paths import GeneralPaths as Gp
from kongru.api_general.universal.funcs.basic_logger import (
    catch_and_log_error,
    catch_and_log_info,
)

# api_nlp
# analysis
from kongru.api_nlp.congruential_analysis.analyzers.demorphy_analyzer import (
    DemorphyAnalyzer,
)
from kongru.api_nlp.congruential_analysis.recognizers.common_entity_recognizer import (
    CommonEntityRecognizer as Cer,
)


class NominalPhraseCongruency:
    """ """

    def __init__(self, morpho_results, save_file_name, file_name):
        self.morpho_results = morpho_results
        self.save_file_name = save_file_name
        self.file_name = file_name.split("/")[-1]  # tatsaechliche Datei

    @staticmethod
    def prepositional_nominal_phrase(
        extracted_info, sentence_np, vocabulary_np, np_demorphy, vocabulary_np_data
    ):

        # Nominal
        head = vocabulary_np[-1]
        demorphy_analyzer = DemorphyAnalyzer()
        inflection_analyzer = demorphy_analyzer

        inflected_word_classes_exist = {"ADJA": False, "ART": False}

        # nach ADJ oder DEF suchen
        for row in extracted_info:
            row = row.split(",")
            if "ART" in row:
                inflected_word_classes_exist["ART"] = True
            if "ADJA" in row:
                inflected_word_classes_exist["ADJA"] = True

        lemma_finder = demorphy_analyzer.get_read_in_lemmas()
        lema_exists = head in lemma_finder

        # Wenn es keine unbestimmen/bestimmten Artikel gibt
        # und der Kopf ist ein Lemma
        # kann man davon ausgehen, dass die NP kongruiert.
        if (
            inflected_word_classes_exist.get("ADJA") is False
            and inflected_word_classes_exist.get("ART") is False
            and lema_exists
        ):
            return "5"

        else:
            try:

                def token_data(token_key=1):

                    try:
                        main_token = vocabulary_np_data.get(token_key).get("noun", "")
                        article = vocabulary_np_data.get(token_key).get("noun", "")
                        number = (
                            vocabulary_np_data.get(token_key)
                            .get("noun_info", "")
                            .get("numerus", "")
                        )
                        gender = (
                            vocabulary_np_data.get(token_key)
                            .get("noun_info", "")
                            .get("genus", "")
                        )
                        case = (
                            vocabulary_np_data.get(token_key)
                            .get("noun_info", "")
                            .get("kasus", "")
                        )

                        return {
                            "main_token": main_token,
                            "article": article,
                            "number": number,
                            "gender": gender,
                            "case": case,
                        }
                    except Exception as e:
                        catch_and_log_error(
                            error=e,
                            custom_message="Key in dem token_data ist nicht vorhanden",
                        )

                prep = token_data()
                head_noun = token_data(2)

                # Paramter zur Bestimmung der Kongruenz weitergeben
                inflection_analyzer.article = head_noun.get("article")
                inflection_analyzer.prepositon = prep.get("main_token")
                inflection_analyzer.number = head_noun.get("number")
                inflection_analyzer.gender = head_noun.get("gender")
                inflection_analyzer.case = head_noun.get("case")

                # analyse durchfuehren
                inflection_result = inflection_analyzer.analyze_indefinite_inflections(
                    demorphy_dict=np_demorphy
                )

                if inflection_result:
                    return "5"
                else:
                    return "99"

            except Exception as e:
                catch_and_log_error(
                    error=e,
                    custom_message="Die Bestimmung über Praeposition konnte nicht "
                    "durchgefuehrt werden",
                )

    @staticmethod
    def art_def_nominal_phrase(extracted_info, sentence, vocabulary, np_demorphy):

        # Nominal
        try:
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
            if (
                demorphy_check
                and bool(word)
                or demorphy_dict
                and demorphy_dict.get(head)
            ):
                return "1"
            else:
                return "0"
        except Exception as e:
            catch_and_log_error(
                error=e,
                custom_message="Np konnte als Art nicht verarbeitet werden. ",
                echo_error=False,
            )
            return "0"

    @staticmethod
    def nominal_phrasing_spelling(vocabulary_np, demorphy_dict):

        phrasing_and_spelling = {
            "demorphy_word": list(),
            "phrase": list(),
            "proper_common": list(),
            "misspelling": list(),
        }

        # Phrasen kontrollieren
        vocabulary_phrase = " ".join(vocabulary_np)
        detecor = Cer(phrases_or_proper=[vocabulary_phrase])
        phrase = detecor.check_common_phrase_or_proper(entity_check="phrase")

        for word in vocabulary_np:
            detecor = Cer(phrases_or_proper=[word])
            demorphy_entry = demorphy_dict.get(word)
            proper_common = detecor.check_common_phrase_or_proper(
                entity_check="proper_common"
            )

            # Boolean aufstellen, um die Ergebnisse zu sortieren
            phrase_exists = bool(phrase)
            proper_common_exists = bool(proper_common)
            demorphy_entry_exists = bool(demorphy_entry is not None)

            # Kategorien aufstellen
            misspelling = (
                not demorphy_entry_exists
                and not proper_common_exists
                and not phrase_exists
            )

            demorphy_words = (
                demorphy_entry_exists and not proper_common_exists and not phrase_exists
            )
            proper_common = demorphy_entry_exists or proper_common_exists

            # Eintraege sortieren
            if misspelling:
                phrasing_and_spelling["misspelling"].append(word)
            elif demorphy_words:
                phrasing_and_spelling["demorphy_word"].append(word)
            elif proper_common:
                phrasing_and_spelling["proper_common"].append(word)
            elif phrase:
                phrasing_and_spelling["phrase"].append(vocabulary_phrase)
                break

        # Eintragart bestimmen

        correct_word = (
            phrasing_and_spelling.get("demorphy_word")
            and not phrasing_and_spelling.get("misspelling")
            and not phrasing_and_spelling.get("phrase")
            and not phrasing_and_spelling.get("proper_common")
        )

        proper_common_correct = phrasing_and_spelling.get(
            "proper_common"
        ) and not phrasing_and_spelling.get("misspelling")

        phrase_correct = phrasing_and_spelling.get(
            "phrase"
        ) and not phrasing_and_spelling.get("misspelling")
        misspelling_only = phrasing_and_spelling.get("misspelling")

        if correct_word:
            return "1"

        elif proper_common_correct:
            return "2"

        elif phrase_correct:
            return "3"

        elif misspelling_only:
            return "4"

    def nominal_congruency_check(
        self, np_info: dict, np_demorphy: list, demorphy_dict: dict
    ):

        try:
            ##########################################
            # Notwendige NP-Informationen aufstellen #
            ##########################################

            # Die Informationen aus den entsprechenden Dictionaries extrahieren
            full_np = np_info.get("full_np")
            sentence_np = np_info.get("sentence")
            vocabulary_np = full_np.split(" ")

            # Die morphologischen Information der einzelnen Woertern extrahieren
            vocabulary_np_data = copy.deepcopy(np_info)
            vocabulary_np_data.pop("full_np")
            vocabulary_np_data.pop("sentence")

            # Die Informationen, die sich in dem NP-Eintrag befinden koennen.
            word_info = ["def", "genus", "kasus", "numerus"]

            """            
            Die morphologischen Informationen werden aus den jeweilien Nps extrahiert
            und hier gespeichert, damit sie nachher in der Ergebniss-Datei mit
            gespeichert werden koennen. 
            """
            complete_noun_info = []
            extracted_info = []

            # Hier wird die Np-Analyse-Methoden festgelegt.
            np_type = dict()

            # Der Wert 'Type' soll in dem Dictionary nicht ueberschrieben werden.
            # Daher der Check
            np_type_exists = np_type.get("TYPE") is not None

            ##############################
            # Analyse auf der Satzebene  #
            ##############################

            # Rechtschreibung ueberpruefen - Notwendig fuer Phrasen und Redewendungen
            phrasing_and_spelling = self.nominal_phrasing_spelling(
                vocabulary_np, demorphy_dict
            )

            if full_np in sentence_np:
                # Eigennamen
                if phrasing_and_spelling == "2":
                    if np_type_exists is False:
                        np_type["TYPE"] = phrasing_and_spelling

                # Phrase z.B. typische Redewendungen, Straßennamen, etc.
                elif phrasing_and_spelling == "3":
                    if np_type_exists is False:
                        np_type["TYPE"] = phrasing_and_spelling

                # Rechtschreibfehler in dem Satz
                elif phrasing_and_spelling == "4":
                    if np_type_exists is False:
                        np_type["TYPE"] = phrasing_and_spelling

            ##############################################
            # Bestimmung der Analyse auf der Wortebene   #
            ##############################################

            # Die noetigen NP-information extrahieren
            for entry in vocabulary_np_data:
                word_entry = vocabulary_np_data.get(entry)

                # Die morphologischen Informationen der jeweileigen NPs.
                noun_info = word_entry.get("noun_info")
                noun = word_entry.get("noun")
                pos = word_entry.get("pos")

                # Wenn ein Eintrag nicht vorhanden ist, wird es mit "_" bestetzt.
                extracted_info = [
                    noun_info.get(morpo_info, "_") for morpo_info in word_info
                ]

                # Informationen zusammenfuehren und daraus einen String machen
                combined_extracted_info = "|".join(extracted_info)
                complete_noun_info.append(
                    ",".join([noun, pos, combined_extracted_info])
                )

                # Die Np-Analyse type bestimmen

                """
                Wenn die NP nict in dem Satz vorkommt, wird sie nicht beruecksichtigt
                und gilt automatisch als unbekannt. Eine NP kann z.B. in einem 
                Satz nicht vorkommen, wenn die Datei nicht korrekt POS-gepaarst.
                wurde. Es werden auch nicht Nps beruecksichtigt, die 
                falsch geschrieben wurden. 
                """

                if full_np in sentence_np and phrasing_and_spelling == "1":

                    # Die Analyse haengt vom ersten Wort ab
                    initial_word = np_info.get(1).get("pos")

                    # NPs, die mit Artikeln anfangen
                    if initial_word == "ART":
                        if np_type.get("TYPE") is None:
                            np_type["TYPE"] = initial_word
                    # NPs, die mit Praepositionen anfangen
                    elif initial_word == "PREP":
                        np_type["TYPE"] = initial_word

            ##############################
            # Ausfuehurung der Analysen  #
            ##############################

            # NP-Typ extrahieren, um die richtige Analyse
            # automatisch bestimmen zu koennen
            congurency_type = np_type.get("TYPE", "99")

            known_congruency = ["ART", "PREP"]
            unknown_congruency = ["2", "99", "4", "3", "1"]

            if congurency_type in unknown_congruency:
                extracted_np_info = [
                    congurency_type,
                    full_np,
                    *complete_noun_info,
                    sentence_np,
                ]

                return extracted_np_info

            elif congurency_type in known_congruency:

                # Wenn die NP mit einem Artikel anfaengt.
                if congurency_type == "ART":
                    try:
                        congruency_result = self.art_def_nominal_phrase(
                            extracted_info, sentence_np, vocabulary_np, np_demorphy
                        )
                    except Exception as e:
                        catch_and_log_error(
                            error=e,
                            custom_message="NP konnte als ART nicht verarbeitet werden.",
                            echo_error=False,
                        )
                        congruency_result = "99"

                    # Die NP-Kongruenz-Information
                    extracted_np_info = [
                        congruency_result,
                        full_np,
                        # morphologische info nach Komma splliten
                        # dann entpacken, damit alles in einer Liste ist.
                        *complete_noun_info,
                        sentence_np,
                    ]

                    return extracted_np_info

                elif congurency_type == "PREP":

                    # Die NP-Kongruenz-Information
                    congruency_result = self.prepositional_nominal_phrase(
                        complete_noun_info,
                        sentence_np,
                        vocabulary_np,
                        np_demorphy,
                        vocabulary_np_data,
                    )

                    extracted_np_info = [
                        congruency_result,
                        full_np,
                        # morphologische info nach Komma splliten
                        # dann entpacken, damit alles in einer Liste ist.
                        *complete_noun_info,
                        sentence_np,
                    ]

                    return extracted_np_info

            else:
                extracted_np_info = [
                    congurency_type,
                    full_np,
                    # morphologische info nach Komma splliten
                    # dann entpacken, damit alles in einer Liste ist.
                    *complete_noun_info,
                    sentence_np,
                ]

                return extracted_np_info

        except Exception as e:
            catch_and_log_error(
                error=e,
                custom_message="Die Analyse konnte nicht erfolgreich"
                "durchgefuehrt werden.",
            )

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
            disable=False,
            desc=f"Die NP-Analyse fuer {self.file_name} durchfuehren...",
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

        catch_and_log_info(
            msg=f"Die NP-Analyse fuer {self.file_name} wurde abgeschlossen...",
            echo_msg=True,
        )

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
                        custom_message=f"{congruency_entry} konnte nicht "
                        f"gespeichert werden.",
                    )


if __name__ == "__main__":
    pass
