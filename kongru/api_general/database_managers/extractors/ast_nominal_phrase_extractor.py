# Standard
import ast
import csv

from io import StringIO

# Pip
# None

# Custom

# universals

# api general

# constants
from kongru.api_general.universal.constants.general_paths import GeneralPaths as Gp
from kongru.api_general.universal.constants.message_keys import MessageKeys as Mk

# funcs
from kongru.api_general.universal.funcs.basic_logger import catch_and_log_error

# Message Keys
general_keys = Mk.General


class AstNominalPhraseExtractor:
    """
    dient zur Extraktion von nominalen Phrasen aus abstrakten Syntaxbaeumen (AST).
    Sie bietet Methoden zum Extrahieren von AST-Daten und zum Speichern dieser Daten
     in einer CSV-Datei.
    """

    def __init__(
        self,
        ast_file_name: str = None,
        save_name: str = None,
        incoming_data: str = None,
        pylist_name: str = None,
    ):
        self.pylist_name = pylist_name
        self.save_name = save_name.replace("ast", "csv")
        self.incoming_data = incoming_data
        self.ast_file_name = ast_file_name

    def get_ast_data(self) -> list:
        """
        Diese Funktion gibt die abstrakten Syntaxbaeume (AST) der eingehenden
        Daten zurueck.

        Beispiel:
        [[['1_1', '1023_0001416_output.txt', 1,
        'M. Meier Müllergasse 1 12345 Stadt X Internationale
        Au-pair Vermittlung Bahnhofstr .',....]]]

        Returns:
            list: Eine Liste der AST-Daten.
        """

        if self.incoming_data:
            virtual_incoming_file = StringIO(str(self.incoming_data)).read()
            data = virtual_incoming_file.replace(r"\ufeff", "")
            ast_data = ast.literal_eval(data)
            ast_data = ast.literal_eval(ast_data[0][0])
            return ast_data

        if self.ast_file_name and not self.pylist_name:
            try:
                file = open(
                    self.ast_file_name,
                    mode="r",
                    encoding="utf-8",
                    errors="ignore",
                ).read()

                data = file.replace("\ufeff", "")
                ast_data = ast.literal_eval(data)

                return ast_data
            except Exception as e:
                catch_and_log_error(
                    error=e,
                    custom_message=general_keys.FILE_MISSING.value,
                    kill_if_fatal_error=True,
                )

        if self.pylist_name:
            file = open(
                f"user/incoming/pylist/{self.pylist_name}.pylist",
                mode="r",
                encoding="utf-8",
                errors="ignore",
            ).read()

            data = file.replace("\ufeff", "")
            ast_data = ast.literal_eval(data)

            return ast_data

    def get_ast_data_overview(self) -> dict:
        """
        Diese Funktion zeigt die abstrakten syntaxbaeume (AST) der eingehenden Daten an.

        Beispiel:
            {1: ['M. Meier', [('M.', 'N', 'Fem|_|Sg'), ('Meier', 'N', 'Fem|_|Sg')],
            .... }

        Returns:
            list: Eine Liste der AST-Daten.
        """

        c = 0
        np_data = {}
        allowed_pos = ["N", "PREP", "ART", "ADJA"]  # not allowed: 'CARD', 'V', 'KON'

        new_data = self.get_ast_data()

        for sentence in new_data:

            for raw in sentence:
                if len(raw) == 7:
                    true_np = ""
                    c += 1
                    mp_morpho_info = []
                    for token in raw[6]:

                        if token[3] in allowed_pos:
                            if token[3] == "PREP":
                                token_data = (
                                    token[1],
                                    token[3],
                                    token[5],
                                )  # case, 'PREP'-tag)

                                mp_morpho_info.append(token_data)
                                np_data[c] = mp_morpho_info
                            else:
                                token_data = (
                                    token[1],
                                    token[3],
                                    token[5],
                                )  # (word form, POS-tag)

                                mp_morpho_info.append(token_data)
                                if isinstance(mp_morpho_info, list):
                                    d = [item[0] for item in mp_morpho_info]
                                    true_np = " ".join(d)

                                if isinstance(raw[2], str):
                                    sentence = raw[2]
                                else:
                                    sentence = raw[3]

                                np_id = raw[0]

                                np_data[c] = [np_id, true_np, mp_morpho_info, sentence]

        return np_data

    def save_extracted_ast_nps(self) -> None:
        """
        Diese Methode speichert die extrahierten AST-Daten in einer CSV-Datei.

        Die Methode ruft 'get_ast_data_overview()' auf, um die AST-Daten abzurufen,
        und speichert sie in einer CSV-Datei
        mit dem in 'self.save_name' angegebenen Namen.
        Die CSV-Datei enthaelt Informationen ueber die AST-Struktur.

        Returns:
        None:
        """
        nps_dict = self.get_ast_data_overview()

        with open(self.save_name, mode="w", encoding="utf-8", newline="") as save:
            csv_writer = csv.writer(save)
            result_set = list()

            for key, values in nps_dict.items():

                try:
                    if isinstance(values[2], list):
                        np_res = [" ".join(tups) for tups in values[2]]
                        np_id = values[0]
                        np = values[1]

                        result_set.append(np_res)

                        np_res.append(values[-1])
                        np_res.insert(0, np)
                        np_res.insert(0, np_id)
                        csv_writer.writerow(np_res)

                except Exception as e:
                    catch_and_log_error(
                        custom_message="Diese NP ist zu kurz, um analysiert zu werden",
                        echo_msg=False,
                        error=e,
                    )

        return None


if __name__ == "__main__":
    pass
