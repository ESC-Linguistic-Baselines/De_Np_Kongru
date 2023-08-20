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
        file_name="/Users/christopherchandler/repo/Python/De_NP_Kongru/user/outgoing/np/test_np_file.csv",
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
        np_id = 0
        np_data = {}
        with open(file_name, mode="r", encoding="utf-8") as file:
            for line in file:
                np_id += 1
                line = line.strip().split(",")

                dict_key = line[0]
                np_info = line[1:]

                key = f"{np_id}_{dict_key}"
                np_data[key] = dict_key, np_info

        return np_data

    def save_congruency_results(congruency_results: dict) -> None:
        """
        Die Ergebnisse der Auswertung speichern.

        Args:
            congruency_results(dict)
             Die Auswertung der Kongruenz der NPs

        Returns:
            None
        """
        with open(
            f"{Gp.RES_SAVE_NP.value}",
            mode="w",
            encoding="utf-8",
        ) as save:
            csv_writer = csv.writer(save, delimiter=",")

            for np in congruency_results:
                case = congruency_results.get(np)[-2]
                demorphy = congruency_results.get(np)[:-2]
                congruency = congruency_results.get(np)[-1]

                results = (np, case, demorphy, congruency)

                csv_writer.writerow(results)

        return None


if __name__ == "__main__":
    res = DemorphyParser().get_read_in_np_file()
    print(res)
