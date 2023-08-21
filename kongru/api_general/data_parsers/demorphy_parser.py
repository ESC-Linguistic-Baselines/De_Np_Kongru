# Standard
import csv

# Pip

# Custom
from kongru.api_general.universal.constants.general_paths import GeneralPaths


class DemorphyParser:
    """ """

    def __init__(
        self,
        demorphy_dict: str = GeneralPaths.DB_DEMORPHY_TXT_TEST.value,
        file_name="/Users/christopherchandler/repo/Python/De_NP_Kongru/user/"
                  "outgoing/np/nps_2023_08_21.csv",
    ):
        self.demorphy_dict = demorphy_dict
        self.file_name = file_name

    def get_read_in_demorphy_dict(self):
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

                line = line[:-1]

                np_id_number += 1
                np_info = line[0].split(",")

                full_np = np_info[0]

                # Die internen NPS durch numerieren und splitten
                internal_np = dict ()
                data_count = 0
                for data in np_info[1:]:

                    data_count+=1
                    if data_count == len(np_info):
                        # Das letzte Element koennte eine Praeposition sein.
                        internal_np["PREP"] = data
                    else:
                        if data != " _":
                            congruency_info = data.split(" ")[-2].split("|")
                            congru = dict()
                            congru["unk"] = []

                            for info in congruency_info:

                                if info in number:
                                    congru["numerus"] = info
                                elif info in gender:
                                    congru["genus"]=info
                                elif info  in case:
                                    congru["kasus"] =info
                                elif info in article:
                                    congru["def"] =info
                                else:
                                    congru["unk"].append(info)

                            internal_np[data_count] = {"noun":data.split(" ")[1],
                                                       "noun_info":congru}

                key = f"{np_id_number}_{full_np}"
                # Die dicts zusaemmenfuehren, damit alle Informationen zusammen
                # gespeichert werden.
                np_data[key] = {"full_np":full_np}|internal_np

        return np_data


if __name__ == "__main__":
    res = DemorphyParser().get_read_in_np_file()

    for row in res:
        print(row)
