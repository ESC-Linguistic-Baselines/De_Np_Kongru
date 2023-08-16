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

    def __get_ast_data(self, file_entry=True):
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
                                np_data[c] = np_value

        # remove 1-token NPs and NPs with PREP at the end
        filtered_np_data = {}
        for key, values in np_data.items():
            if len(values) > 1:
                if values[-1][1] == "PREP":
                    if len(values) > 2:
                        filtered_np_data[key] = values[:-1]
                    else:
                        pass
                else:
                    filtered_np_data[key] = values

        return filtered_np_data

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

            for key, values in nps_dict.items():
                tokens = []
                pure_NP = []

                # required case for NPs (if available)
                if values[0][1] == "PREP":
                    case = values[0][0].lower()
                else:
                    case = "_"

                for value in values:
                    if value[1] != "PREP":
                        tokens.append(" ".join(value))
                        pure_NP.append(value[0])
                    else:
                        pass

                # e.g.  der Hund (whole NP) + der ART, Hund N (tokens) + nom (required case)
                result = [" ".join(pure_NP)] + tokens + [case]

                csv_writer.writerow([", ".join(result)])

        return None


if __name__ == "__main__":
    pass
