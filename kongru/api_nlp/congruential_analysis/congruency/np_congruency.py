# Standard
import csv
import types
import traceback

import typer

# Pip
# None

# Custom
from kongru.api_nlp.congruential_analysis.analyzers.demorphy_analyzer import DemorphyAnalyzer
from kongru.api_nlp.congruential_analysis.analyzers.common_entity_recognition import (
    CommonEntityRecognition as Cer)
from kongru.api_general.universal.constants.general_paths import GeneralPaths as Gp
from kongru.api_general.universal.funcs.basic_logger import get_logger, set_up_logger


class NpCongruency:
    def __init__(self, morpho_results, save_file_name = ""):
        self.morpho_results = morpho_results
        self.save_file_name = save_file_name


    def art_def_nominal_phrase(self, extracted_info, sentence, vocabulary, np_demorphy):

        # Nominal
        head = vocabulary[-1]
        res =  DemorphyAnalyzer().guess_noun_by_suffix(head)

        _, np_genus, np_kasus, np_numerus, = extracted_info

        demorphy_check = 0


        for demoprhy_enty in np_demorphy[1][1]:
            demoprhy_enty = demoprhy_enty.replace(" ", ",")
            entry = demoprhy_enty.split(",")

            noun_demorph, pos_demorph, genus_demorph, kasus_demorph, numerus_demorph = entry
            numerus_demorph = numerus_demorph.replace("plu", "pl")

            np_morph = (np_genus,np_kasus, np_numerus)
            np_demorph = (genus_demorph,kasus_demorph,numerus_demorph)

            np_morph = [i.lower() for i in np_morph]
            np_demorph = [i.lower() for i in np_demorph]
            demorphy_check = np_morph==np_demorph

            if demorphy_check:
                break

        # Exisitiert das Wort in dem Woerterbuch
        demorphy_dict = DemorphyAnalyzer().get_read_in_demorphy_dict(True)
        word = demorphy_dict.get(res[0])

        if demorphy_check and bool(word):
            return "1"
        else:
            return "0"

        pass


    def  nominal_congruency_check(self, np_info: dict, np_demorphy:list ):

        try:
            full_np = np_info.get("full_np")
            sentence = np_info.get("sentence")
            vocabulary = full_np.split(" ")

            # Np info aufstellen
            np_morphological_info = list(np_info.values())

            complete_noun_info = []
            np_type = dict()

            # Die noetigen NP-information extrahieren
            for row in np_morphological_info:

                # Es gibt einzelne Strings, die ignoriert werden sollen.
                if isinstance(row, dict):
                    noun_info = row.get("noun_info")
                    noun = row.get("noun")
                    pos = row.get("pos")

                    # Die Informationen, die sich in dem NP-Eintrag befinden koennen
                    word_info = ['def','genus', 'kasus', 'numerus']
                    extracted_info = [noun_info.get(morpo_info,"_") for morpo_info in word_info]
                    combined_extracted_info = "|".join(extracted_info)
                    complete_noun_info.append(" ".join([noun,pos, combined_extracted_info]))

                    # Die Np-Analyse type bestimmen
                    if full_np in sentence:
                        # NPs die mit Artikeln anfangen
                        if np_info.get(1).get("pos") == "ART":

                            np_type["TYPE"] = {
                                "ART":True
                            }
                            break
                        else:

                            np_type["TYPE"] = "99"
                            break

                    else:
                        np_type["TYPE"] = "99"


            combined_complete_noun_info = ",".join(complete_noun_info)
            congurency_type = np_type.get("TYPE")

            if congurency_type == "99":
                extracted_np_info = [congurency_type, full_np,
                                     # morphologische info nach Komma splliten
                                     # dann entpacken, damit alles in einer Liste ist.
                                     *combined_complete_noun_info.split(","),
                                     sentence]

                return extracted_np_info

            if congurency_type.get("ART",False) is True:
                congruency_result = self.art_def_nominal_phrase(
                    extracted_info, sentence, vocabulary, np_demorphy)

                # Die NP-Kongruenz-Information, die in einem
                extracted_np_info = [congruency_result, full_np,
                                     # morphologische info nach Komma splliten
                                     # dann entpacken, damit alles in einer Liste ist.
                                     *combined_complete_noun_info.split(",") ,
                                     sentence]

                return extracted_np_info


        except Exception as e:
            logger =  get_logger()
            custom_message = "___"
            traceback_str = traceback.format_exc()
            logger.error(e, extra={"custom_message": custom_message})
            typer.echo(e)
            traceback.print_exc()


    def run_congruency_check(self):
        """

        """
        morpho_results = self.morpho_results
        np_data, np_morph = morpho_results.get("np_data"), \
            morpho_results.get("np_morph")

        congruency_results = dict()

        for np in np_data:

            np_info = np_data.get(np)
            np_demorphy = np_morph.get(np)

            if np_info:
                result = self.nominal_congruency_check(np_info=np_info,
                                                      np_demorphy=np_demorphy)

                if result is None:
                    result = "99"

                congruency_results[np]=result

        return congruency_results


    def save_congruency_results(self) -> None:
        """

        """

        with open(
            f"{Gp.RES_SAVE_NP.value}_{self.save_file_name}",
            mode="w",
            encoding="utf-8",
        ) as save:
            csv_writer = csv.writer(save, delimiter=",")

            congruency_results = self.run_congruency_check()
            for row in congruency_results:
                try:
                    res = congruency_results.get(row)
                    csv_writer.writerow(res)

                except Exception as e:
                    set_up_logger(error=e,
                                  custom_message=f"{row} konnte nicht gespeichert werden")

        return None

if __name__ == "__main__":
    pass
