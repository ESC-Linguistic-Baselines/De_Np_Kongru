# Standard
import ast
import csv

# Pip
# None

# Custom
from kongru.api_general.universal.constants.general_paths import GeneralPaths as Gp


class NpFileHandler:
    def __init__(self, file_name: str, save_name: str = Gp.RES_AST_NP_FILE.value):
        self.file_name = file_name
        self.save_name = save_name

    def __get_ast_data(self, file_entry=True) -> list:
        if file_entry:
            file = open(
                self.file_name, mode="r", encoding="utf-8", errors="ignore"
            ).read()
            data = file
        else:
            data = self.file_name

        data = data.replace("\ufeff", "")
        new_data = ast.literal_eval(data)

        return new_data

    def get_ast_data_overview(self) -> dict:
        """
        Die NP-Datei, die ausgewertet werden soll, wird hier eingelesen.

        Args:
            file_name (str): die NP-datei, die eingelesen werden soll.

        Returns:
            np_file (list): eine Liste der NPs, die aus der eingelesenen Datei
              extrahiert wurden
        """
        c = 0
        np_data = {}
        allowed_pos = ["N", "PREP", "ART", "ADJA"]  # not allowed: 'CARD', 'V', 'KON'
        raw_sentence = dict()

        new_data = self.__get_ast_data()
        for sentence in new_data:
            for raw in sentence:
                if len(raw) == 7:

                    c += 1
                    np_value = []
                    for token in raw[6]:

                        if token[3] in allowed_pos:
                            if token[3] == "PREP":
                                token_data = (
                                    token[1],
                                    token[3],
                                    token[5],
                                )  # case, 'PREP'-tag)

                                np_value.append(token_data)
                                np_data[c] = np_value
                            else:
                                token_data = (
                                    token[1],
                                    token[3],
                                    token[5],

                                )  # (word form, POS-tag)

                                np_value.append(token_data)
                                if isinstance(np_value, list):
                                    d = [item[0] for item in np_value]
                                    true_np = " ".join(d)

                                np_data[c] = [true_np, np_value,raw[3]]


        return np_data

    def save_nps(self):  # [last update: 12.07.2023 - Georg]
        """
        Saving all NPs to a csv file.
        Each NP per line in the format:
        whole pure NP, Token-1 POS-tag-1, ..., Token-x POS-tag-x, required case
        e.g.
        der Hund, der ART, Hund N, nom
        eine kleine Katze, eine ART, kleine ADJA, Katze N, _

        Arg:
            nps_dict(dict): The dict from read_in_np_file_as_ast

        Returns:
            None
        """

        nps_dict = self.get_ast_data_overview()
        with open(self.save_name, mode="w", encoding="utf-8", newline="") as save:
            csv_writer = csv.writer(save)
            result_set = list()
            for key, values in nps_dict.items():

                if isinstance(values[1], list):
                    res = [' '.join(tups) for tups in values[1]]

                    result_set.append(res)
                    res.append(values[-1])
                    res.insert(0,values[0])
                    csv_writer.writerow(res)

        return None

if __name__ == "__main__":
    res = NpFileHandler(
        "/Users/christopherchandler/repo/Python/"
        "De_NP_Kongru/user/incoming/ast/1023_0001416.txt"
    ).get_ast_data_overview()
    print(res)