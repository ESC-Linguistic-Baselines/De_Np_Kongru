# Standard
import csv
import pickle

# Pip
# None

# Custom

# api_general

# constants
from kongru.api_general.universal.constants.general_paths import GeneralPaths as Gp


class DemorphyManager:
    """ """

    def __init__(
        self,
        file_name=Gp.TEST_NP_FILE_CSV.value,
    ):
        self.demorphy_dict = Gp.DB_DEMORPHY_TXT.value
        self.lemma_txt = Gp.DB_DEMORPHY_LEMMA_TXT.value
        self.file_name = file_name

    def get_read_in_demorphy_dict(self, read_in_pickle_dict: bool = True):
        """
        Reading the morphological dictionary.

        Args:
            filename (str): the morphological dict to be read.

        Returns:
            morpho_dict (dict): the morphological dictionary, which has been read:
            e.g.
            morpho_dict = {'der' : 'die ART,noGender,gen,plu,<def>,strong ... die ART,masc,nom,sing,<def>,strong',
                           'kleiner' : 'klein ADJ,fem,gen,sing,pos,strong ... klein ADJ,fem,dat,sing,pos,strong'
                            ...,
                           'Hund' : 'Hund NN,masc,acc,sing ... Hund NNP,noGender,acc,sing'}
        """

        if read_in_pickle_dict is False:
            demorphy_dict_data = {}

            with open(self.demorphy_dict, mode="r", encoding="utf-8") as out_going:
                data = out_going.readlines()
                for row in data:
                    row_data = row.strip().split(" ")
                    if len(row_data) == 1:
                        key = row.strip()
                        demorphy_dict_data[key] = []
                    else:
                        demorphy_dict_data[key].append(row.strip())

            return demorphy_dict_data

        else:
            with open(Gp.DB_DEMORTHY_PKL.value, "rb") as pickle_file:
                data = pickle.load(pickle_file)
                return data

    def get_read_in_np_file(self) -> dict:
        """
        Die NP-Datei, die ausgewertet werden soll, wird hier eingelesen.

        Args:
            file_name (str): die NP-datei, die eingelesen werden soll.

        Returns:
            np_file (list): eine Liste der NPs, die aus der eingelesenen Datei
              extrahiert wurden
        """
        file_name = self.file_name
        np_id_number = 0
        np_data = {}

        case = "Acc", "Dat", "Nom", "Gen"
        gender = "Fem", "Neut", "Masc"
        number = "Pl", "Sg"
        article = "Def", "Indef"

        with open(file_name, mode="r", encoding="utf-8") as file:
            csv_reader = csv.reader(file)

            for line in csv_reader:
                # Die internen NPS durch numerieren und splitten
                internal_np = dict()

                np_id_number += 1
                data_count = 0

                basic_np = line[0]
                np_morpho_info = line[1:-1]
                sentence = line[-1]

                for entry in np_morpho_info:
                    data_count += 1

                    np_morpho_entry_data = entry.split()
                    np, pos, morpho_info = np_morpho_entry_data
                    congruency_info = morpho_info.split("|")

                    congru = dict()
                    congru["unk"] = []

                    for info in congruency_info:

                        if info in number:
                            congru["numerus"] = info
                        elif info in gender:
                            congru["genus"] = info
                        elif info in case:
                            congru["kasus"] = info
                        elif info in article:
                            congru["def"] = info
                        else:
                            congru["unk"].append(info)

                    internal_np[data_count] = {
                        "noun": np,
                        "pos": pos,
                        "noun_info": congru,
                    }

                key = f"{np_id_number}_{basic_np}"

                # Die dicts zusaemmenfuehren, damit alle Informationen zusammen
                # gespeichert werden.
                np_data[key] = {"full_np": basic_np, "sentence": sentence} | internal_np

        return np_data

    def get_read_in_lemmas(self) -> list:
        with open(self.lemma_txt, mode="r", encoding="utf-8") as file:
            lemmas = [lemma.replace("\n", "") for lemma in file.readlines()]
            return lemmas


if __name__ == "__main__":
    res = DemorphyManager().get_read_in_np_file()
