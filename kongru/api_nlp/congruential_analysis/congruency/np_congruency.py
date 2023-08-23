# Standard
import csv

import typer

# Pip
# None

# Custom
from kongru.api_nlp.congruential_analysis.analyzers.demorphy_analyzer import DemorphyAnalyzer
from kongru.api_general.universal.constants.general_paths import GeneralPaths as Gp
from kongru.api_general.universal.funcs.basic_logger import get_logger

class NpCongruency:
    def __init__(self, morpho_results):
        self.morpho_results = morpho_results
        self.np_article = {
            "masc": ["der", "den", "dem", "des"],
            "fem": ["die", "die", "der", "der"],
            "neut": ["das", "das", "dem", "des"],
            "plural": ["die", "die", "den", "der"],
        }
        self.article_codes = {0: "nom", 1: "acc", 2: "dat", 3: "gen"}


    def art_def_nominal_phrase(self, extracted_info, sentence, vocabulary, np_demorphy):

        # Nominal
        w = vocabulary[1]
        res =  DemorphyAnalyzer().guess_word_by_suffix(w)

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

        print(vocabulary, extracted_info)

        pass


    def nominal_congruency_check(self, np_info: dict, np_demorphy:list ):

        try:
            full_np = np_info.get("full_np")
            sentence = np_info.get("sentence")
            vocabulary = full_np.split(" ")

            # Np info aufstellen
            np_morphological_info = list(np_info.values())
            complete_noun_info = []
            np_type = []

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

                    # Unvollstaendige NPs werden nicht beruecksichtigt.
                    if full_np in sentence:
                        if pos == "ART":
                            np_type.append("ART")




            congruency = "UNK"
            combined_complete_noun_info = ",".join(complete_noun_info)
            extracted_np_info = [congruency, full_np, combined_complete_noun_info , sentence]

            congruency_type_check = {"ART":self.art_def_nominal_phrase}

            congruency_result = congruency_type_check.get("ART")(
                extracted_info, sentence, vocabulary, np_demorphy)
            print(congruency_result)


            return extracted_np_info

        except Exception as e:
            logger =  get_logger()
            custom_message = "___"
            logger.error(e, extra={"custom_message": custom_message})
            typer.echo(e)

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
                self.nominal_congruency_check(np_info=np_info,
                                                      np_demorphy=np_demorphy)

        return {"":""}


    def save_congruency_results(self) -> None:
        """

        """
        with open(
            f"{Gp.RES_SAVE_NP.value}",
            mode="w",
            encoding="utf-8",
        ) as save:
            csv_writer = csv.writer(save, delimiter=",")

            congruency_results = self.run_congruency_check()
            for row in congruency_results:
                join = congruency_results.get(row)
                csv_writer.writerow(join)

        return None


if __name__ == "__main__":
    pass
