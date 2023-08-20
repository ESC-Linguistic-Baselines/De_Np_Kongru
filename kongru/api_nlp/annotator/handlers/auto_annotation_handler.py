# Standard
import ast
import json

# Pip
# None

# Custom


class AutoAnnotation:
    def __init__(self, file_name: str):
        self.file_name = file_name

    def __build_np_dict(self):
        np_dict = {
            "author": {"learner_id": "", "lvl": ""},
            "NP_info": {
                "file_ID": "",  # nr to id og file
                "sent_NP_ID": "",  # nr to id og NP and sentence
                "target_syntax": "",  # is target syntax recognizable?
                "lexicalised": "",  # is expression fixed (ie greeting)
                "len_np": "",  # ggf
                "comment_NP": "",
            },
            "TOK_info": {},
            "syntax_info": {},
        }

        return np_dict

    def __build_TOK_dict(self):
        """
        Function to build basic dictionary frame for a single TOK in an NP
        Return:
        1. tok_dict (dict): dictionary for token info
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

    def __build_rel_dict(self):
        """Function to build a syntactic relationship dictionary frame
        for two tokens from an NP
        Return:
        1. rel_dict (dict): dictionary for syntax info

        """

        rel_dict = {
            "rel_type": "",
            "source_TOK": "",
            "target_TOK": "",
            "target_case": {"requires_case": "", "found_case": "", "agrees?": ""},
        }

        return rel_dict

    def __get_tok_info(self, np_dict, np, i):
        """Function to supply np and token info provided by input file
        as well as starting to infer syntactic information to add to np_dict.
        Input:
        1. np_dict (dict): dict of a single NP
        2. np (list): list representation from input file of a single NP
        3. i (int): index position of relevant token in NP
        Return:
        1. np_dict (dict): dict of a single NP with token info from input file
        """

        # get tok id name & build token dict
        tok_id = "TOK" + str(i + 1)
        np_dict["TOK_info"][tok_id] = self.__build_TOK_dict()

        # get word form, lexeme, POS tag, inflection info
        np_dict["TOK_info"][tok_id]["word_form"] = np[6][i][1]
        np_dict["TOK_info"][tok_id]["lexeme"] = np[6][i][2]
        np_dict["TOK_info"][tok_id]["POS_tag"] = np[6][i][4]
        np_dict["TOK_info"][tok_id]["inflection"] = np[6][i][5]

        # get id name of syntactic relationship
        rel_id = "rel_" + str(len(np_dict["syntax_info"]) + 1)

        # if token is dominated by a regens (!=0) with within the same np,
        # built syntax relationship dictionary and infer type
        for token in np[6]:
            if token[0] == np[6][i][6] and np[6][i][6] != "0":
                np_dict["syntax_info"][rel_id] = self.__get_syntax_info(np[6][i], np)

        ### function tag?, np[6][i][7]

        return np_dict

    def __get_syntax_info(self, tok, np):
        """Function to infer syntax info based on data from input file
        Input:
        1. tok (tuple): token (dependens) info from input
        2. np (list): np info from input representation
        Return:
        1.relx_dict (dict): dict with infered syntax info between two tokens
        """
        # initiate empty syntax relationship dict
        relx_dict = self.__build_rel_dict()

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
                    single_np_dict = self.__build_np_dict()

                    # get file & setence ID
                    single_np_dict["NP_info"]["file_ID"] = np[1]
                    single_np_dict["NP_info"]["sent_NP_ID"] = np[0]

                    ### get len of NP/number of tokens in NP?
                    single_np_dict["NP_info"]["len_np"] = len(np[-1])

                    # for tok in NP: build TOK-X dictionary
                    # and infer syntactic relations
                    for i, tok in enumerate(np[6]):
                        np_dict_TOK = self.__get_tok_info(single_np_dict, np, i)

                    # collect nps from single sentence
                    sent_nps.append(np_dict_TOK)

                # collect sentences from file
                all_nps_infile.append(sent_nps)

        #### example output for nps in sentence ##########
        for x in all_nps_infile[5]:
            print(x, "\n")

        # json convert
        json_format = json.dumps(all_nps_infile)


if __name__ == "__main__":
    file = AutoAnnotation(
        file_name="/Users/christopherchandler/repo/Python/De_NP_Kongru/user/incoming/ast/1023_0001416.txt"
    )
    print(file.run_auto_annotation())
