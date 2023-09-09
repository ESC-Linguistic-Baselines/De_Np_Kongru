# Standard
import ast
import json

# Pip
# None

# Custom
# None


class AutoAnnotation:
    """
    Die Klasse `AutoAnnotation` dient zur automatisierten Annotation von
     syntaktischen Informationen in Textdaten.
    """

    def __init__(self, file_name: str):
        self.file_name = file_name

    @staticmethod
    def build_np_dict() -> dict:
        """
        Diese Methode erstellt ein leeres dict zur Darstellung von Informationen
        ueber eine nominale Phrase (NP).

        Beispiel:
            {
            "author": {"learner_id": "", "lvl": ""},
            "NP_info": {
                "file_ID": "",         # Dateinummer zur Identifikation der Datei
                "sent_NP_ID": "",      # Nummer zur Identifikation der NP und des Satzes
                "target_syntax": "",   # Ist die Zielsyntax erkennbar?
                "lexicalised": "",     # Ist der Ausdruck festgelegt (z.B., Begrüßung)?
                "len_np": "",          # Länge der NP (ggf. Anzahl der Tokens)
                "comment_NP": ""       # Kommentar zur NP
            },
            "TOK_info": {},            # Informationen über Tokens in der NP (leeres dict)
            "syntax_info": {}          # Informationen zur Syntax (leeres dict)
            }

        Returns:
            np_dict (dict) Ein leeres dict mit vordefinierten Schlüsseln und
             Platzhaltern fuer Informationen über die NP.

        """

        np_dict = {
            "author": {"learner_id": "", "lvl": ""},
            "NP_info": {
                "file_ID": "",  # Dateinummer zur Identifikation der Datei
                "sent_NP_ID": "",  # Nummer zur Identifikation der NP und des Satzes
                "target_syntax": "",  # Ist die Zielsyntax erkennbar?
                "lexicalised": "",  # Ist der Ausdruck festgelegt (z.B., Begrüßung)?
                "len_np": "",  # Länge der NP (ggf. Anzahl der Tokens)
                "comment_NP": "",  # Kommentar zur NP
            },
            "TOK_info": {},  # Informationen ueber Tokens in der NP (leeres dict)
            "syntax_info": {},  # Informationen zur Syntax (leeres dict)
        }

        return np_dict

    @staticmethod
    def build_TOK_dict() -> dict:
        """
        Diese Methode erstellt das grundlegende dict-Framework fuer
        ein einzelnes Token innerhalb einer NP.

        Beispiel:
            tok_dict = {
                "word_form": "",
                "lexeme": "",
                "orth_target": "",
                "gr_target": "",
                "status": "",
                "POS_tag": "",  # ie ADP/NN
                #   "role_tag": "",         # subj/obj oä tag
                "inflection": "",  # tuple list [("nom","masc", "sg", "def/indef"), ]
                "comment": "",
            }

        Returns:
            tok_dict(dict): Ein dict, das Informationen über ein Token enthaelt.
        """
        # add TOK-X info dict to np dict
        tok_dict = {
            "word_form": "",
            "lexeme": "",
            "orth_target": "",
            "gr_target": "",
            "status": "",
            "POS_tag": "",  # ie ADP/NN
            #   "role_tag": "",         # subj/obj oä tag
            "inflection": "",  # tuple list [("nom","masc", "sg", "def/indef"), ]
            "comment": "",
        }

        return tok_dict

    @staticmethod
    def build_rel_dict():
        """
        Diese Methode erstellt das grundlegende dict-Framework fuer
        eine syntaktische Beziehung zwischen zwei Tokens innerhalb einer NP.

        Beispiel:
        rel_dict = {
        "rel_type": "",
        "source_TOK": "",
        "target_TOK": "",
        "target_case": {"requires_case": "", "found_case": "", "agrees?": ""},
        }

        Returns:
        rel_dict: (dict), das Informationen ueber eine syntaktische Beziehung enthaelt.
        """

        rel_dict = {
            "rel_type": "",
            "source_TOK": "",
            "target_TOK": "",
            "target_case": {"requires_case": "", "found_case": "", "agrees?": ""},
        }

        return rel_dict

    def __get_tok_info(self, np_dict: dict, np: list, i: int) -> dict:
        """
        Diese Methode liefert Informationen über eine nominale Phrase (NP) und Token,
        die von einer Eingabedatei bereitgestellt werden, und beginnt damit,
        syntaktische Informationen für 'np_dict' hinzuzufügen.

        Args:
            np_dict (dict): Ein dict, das eine einzelne NP repräsentiert.
            np (list): Eine Listenrepräsentation einer einzelnen NP aus der Eingabedatei.
            i (int): Indexposition des relevanten Tokens in der NP.

        Returns:
            np_dict (dict) Ein aktualisiertes dict, das die NP mit den Tokeninformationen
             aus der Eingabedatei enthält.
        """

        # get tok id name & build token dict
        tok_id = "TOK" + str(i + 1)
        np_dict["TOK_info"][tok_id] = self.build_TOK_dict()

        # get word form, lexeme, POS tag, inflection info
        np_dict["TOK_info"][tok_id]["word_form"] = np[6][i][1]
        np_dict["TOK_info"][tok_id]["lexeme"] = np[6][i][2]
        np_dict["TOK_info"][tok_id]["POS_tag"] = np[6][i][4]
        np_dict["TOK_info"][tok_id]["inflection"] = np[6][i][5]

        # get id name of syntactic relationship
        rel_id = "rel_" + str(len(np_dict["syntax_info"]) + 1)

        # if token is dominated by a regens (!=0) with within the same np,
        # built syntax relationship dict and infer type
        for token in np[6]:
            if token[0] == np[6][i][6] and np[6][i][6] != "0":
                np_dict["syntax_info"][rel_id] = self.get_syntax_info(np[6][i], np)

        return np_dict

    def get_syntax_info(self, tok, np) -> dict:
        """
        Funktion zur Ableitung von Syntaxinformationen basierend auf Daten aus einer
        Eingabedatei
        Arg:
            tok (Tuple): Token (Abhaengigkeits-) Informationen aus der Eingabe
            np (Liste): NP-Informationen aus der Eingabedarstellung
        Return:
            relx_dict (dict): dict mit abgeleiteten Syntaxinformationen zwischen
            zwei Tokens
        """
        # initiate empty syntax relationship dict
        relx_dict = self.build_rel_dict()

        # match regens id given in dependens representation (tok[6])
        # to a token's id (token[0]) in np
        for token in np[6]:
            if token[0] == tok[6]:
                regens = token

                # add directionality of syntactic relation
                relx_dict["source_TOK"] = regens[1]
                relx_dict["target_TOK"] = tok[1]

                ######### to be refined with morpho info(?) ##################

                # determine relation type via possible POS tags:
                # NN, NE, FM, VAFIN, KON, APPR, VVFIN, VVINF, APPR

                # very basic distinction; i.e. APPR and KON; and the "determines_case"
                # route need special treatment as the regens themselves lack
                # inflection info  & wont lead to agreement
                if regens[4] in ["NE", "NN", "ADJ", "DET", "PPOS", "KON"]:
                    relx_dict["rel_type"] = "must_agree"
                    relx_dict["target_case"]["requires_case"] = regens[5]
                    relx_dict["target_case"]["found_case"] = tok[5]

                elif regens[4] in ["ADP", "VVFIN", "VAFIN", "VVINF", "APPR"]:
                    relx_dict["rel_type"] = "determines_case"
                    relx_dict["target_case"]["requires_case"] = regens[
                        5
                    ]  # too simplistic in this case
                    relx_dict["target_case"]["found_case"] = tok[5]

                else:
                    pass  # POS unknown

                # agreement check; possibly extend to tuple/list for
                # multiple possible inflection options (ambiguous forms)
                if (
                    relx_dict["target_case"]["requires_case"]
                    == relx_dict["target_case"]["found_case"]
                ):
                    relx_dict["target_case"]["agrees?"] = 1

                else:
                    relx_dict["target_case"]["agrees?"] = 0

        return relx_dict

    def run_auto_annotation(self):

        # read output file
        with open(
            self.file_name, mode="r", encoding="utf-8-sig"
        ) as f:  # utf-8-sig to avoid BOM error
            text = ast.literal_eval(
                f.read().strip()
            )  # ast.literal_eval: interpret string as python syntax

        all_nps_infile = list()

        # iterate through sentences in output file
        for sent in text:
            sent_nps = list()

            # skip empty entries
            if len(sent) > 1:
                # iterate through NPs in each sentence
                for np in sent:

                    # initiate NP dict
                    single_np_dict = self.build_np_dict()

                    # get file & setence ID
                    single_np_dict["NP_info"]["file_ID"] = np[1]
                    single_np_dict["NP_info"]["sent_NP_ID"] = np[0]

                    ### get len of NP/number of tokens in NP?
                    single_np_dict["NP_info"]["len_np"] = len(np[-1])

                    # for tok in NP: build TOK-X dict
                    # and infer syntactic relations
                    for i, tok in enumerate(np[6]):
                        np_dict_TOK = self.__get_tok_info(single_np_dict, np, i)

                    # collect nps from single sentence
                    sent_nps.append(np_dict_TOK)

                # collect sentences from file
                all_nps_infile.append(sent_nps)

        #### example output for nps in sentence ##########
        for x in all_nps_infile:
            print(x, "\n")


if __name__ == "__main__":
    pass
