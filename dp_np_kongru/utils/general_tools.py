# Standard
import ast
import csv
import pickle

# Pip
# None

# Custom
from typing import Any


def read_in_np_file(file_name: str) -> dict:
    """
    Die NP-Datei, die ausgewertet werden soll, wird hier eingelesen.

    Args:
        file_name (str): die NP-datei, die eingelesen werden soll.

    Returns:
        np_file (list): eine Liste der NPs, die aus der eingelesenen Datei
          extrahiert wurden
    """
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
    print(np_data)
    return np_data


def read_in_np_file_as_ast(file_name):  # [last update: 12.07.2023 - Georg]
    """
    Reading of NPs extracted data files and saving the necessary information for future work.

    Arg:
        filename(str): output_exported_nps.txt file

    Returns:
        filtered_np_data(dict): all possible NPs in dictionary and their characterization (POS-tags and required case)
    """
    file = open(file_name, mode="r", encoding="utf-8", errors="ignore").read()

    data = file
    data = data.replace("\ufeff", "")

    new_data = ast.literal_eval(data)

    c = 0
    np_data = {}
    allowed_pos = ["N", "PREP", "ART", "ADJA"]  # not allowed: 'CARD', 'V', 'KON'

    for sentence in new_data:
        for raw in sentence:
            if len(raw) == 7:
                c += 1
                np_value = []
                for token in raw[6]:
                    if token[3] in allowed_pos:
                        if token[3] == "PREP":
                            token_data = (token[5], token[3])  # case, 'PREP'-tag)
                            np_value.append(token_data)
                            np_data[c] = np_value
                        else:
                            token_data = (token[1], token[3])  # (word form, POS-tag)
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


def save_nps(nps_dict):  # [last update: 12.07.2023 - Georg]
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
    with open("nps.csv", mode="w", encoding="utf-8", newline="") as save:
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

            # e.g.   der Hund (whole NP) + der ART, Hund N (tokens) + nom (required case)
            result = [" ".join(pure_NP)] + tokens + [case]

            csv_writer.writerow([", ".join(result)])

    return None


def read_morpho_dict(filename, pickle_file=False, use_pickle_file=True):
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

    morph_dict = {}
    with open(filename, "r") as file:
        lines = file.readlines()
        key = ""
        value = ""
        for line in lines:
            line = line.strip()
            if line.isalpha():
                if key:
                    morph_dict[key] = value.strip()
                key = line
                value = ""
            else:
                value += line + "\n"
        # Save the last key-value pair
        if key:
            morph_dict[key] = value.strip()

    if pickle_file:
        with open(
            "dp_np_kongru/app_resources/data/morph_dict_data/DE_morphy_dict_pickle.pkl",
            mode="wb",
        ) as pk:
            pickle.dump(morph_dict, pk)

    if use_pickle_file:
        pickle.load(
            open(
                "dp_np_kongru/app_resources/data/morph_dict_data/DE_morphy_dict_pickle.pkl",
                mode="rb",
            )
        )

    return morph_dict


def list_flattener(nested_list, set_or_list=list()):
    flattened_list = [item for sublist in nested_list for item in sublist]

    if isinstance(set_or_list, list):
        return flattened_list
    elif isinstance(set_or_list, set):
        return set(flattened_list)


def tokenizer_parse_np(np_data: list) -> list[list()]:
    """
    Die Daten aus der eingelesen NP-Datei einlesen und entsprechend parsen.

    Args:
        np_data (list): eine Liste der NPS, die tokenisert werden sollen.

    Returns:
        np_list_tokenize list[list()]:
           eine Liste von Listen, die die tokenisierten NPS enthalten.
    """

    np_list_tokenized = list([])
    return np_list_tokenized


def find_np_morphology(morph_dict: dict, np_data: dict[str, tuple]) -> dict:
    """
    Find all tokens from NP in the dictionary.

    Args:
        morph_dict (dict): the morphological dictionary
        np_data (dict[str,tuple]): the dict of tokens in NP

    Returns:
        np_morph (dict): infomation about the possible morphological
        characteristics of each token from NP:
        e.g.
        morph_dict = {['kleine': [['klein ADJ', 'noGender', 'nom', 'plu', 'pos',
                     'strong'],
                      ['klein ADJ', 'neut', 'acc', 'sing', 'pos', 'weak'],
                      ['klein ADJ', 'fem', 'nom', 'sing', 'pos'],
                      ['klein ADJ', 'noGender', 'acc', 'plu', 'pos', 'strong'],
                      ['klein ADJ', 'neut', 'nom', 'sing', 'pos', 'weak'],
                      ['klein ADJ', 'fem', 'acc', 'sing', 'pos'],
                      ['klein ADJ', 'masc', 'nom', 'sing', 'pos', 'weak']],
                        ...,
                       'Hund': [['Hund NN', 'masc', 'acc', 'sing'],
                       ['Hund NNP', 'noGender', 'dat', 'sing'],
                       ['Hund NN', 'masc', 'dat', 'sing'],
                       ['Hund NNP', 'noGender', 'nom', 'sing'],
                       ['Hund NN', 'masc', 'nom', 'sing'],
                       ['Hund NNP', 'noGender', 'acc', 'sing']]}
    """

    np_morph = {}
    values_list = []
    c = 0

    for key in np_data:

        np, data = np_data.get(key)
        np_info, case = data[:-1], data[-1]
        np_morph[np] = dict()
        np_split = np.split(" ")

        for tok in np_split:
            c += 1

            if tok in morph_dict:
                np_morph[np][tok] = list()
                lines = morph_dict[tok].split("\n")
                for line in lines:
                    line = line.strip()
                    if line:
                        values_list.append(line.split(","))
                    np_morph[np][tok] = values_list
                values_list = list()

            np_morph[np]["case"] = case
            np_morph[np]["np_data"] = data

    return np_morph


def filter_np_morphology(np_morph: dict) -> dict:
    """
    Filter morphological information of each token.
    The following information stays: [POS, gender, case, number].
    The allowed POS are selected by the user.
    Coincidences are also excluded from the final lists.

    Args:
        np_morph (dict): raw possible morphological characteristic of each token from NP

    Returns:
        np_morph_filtered (dict): POS, gender, case and number only (coincidences are also excluded):
        e.g.
        np_morph_filtered = {['kleine': [['noGender', 'nom', 'plu'],
                            ['neut', 'acc', 'sing'],
                            ['fem', 'nom', 'sing'],
                            ['noGender', 'acc', 'plu'],
                            ['neut', 'nom', 'sing'],
                            ['fem', 'acc', 'sing'],
                            ['masc', 'nom', 'sing']],
                            ...,
                            'Hund': [['masc', 'acc', 'sing'],
                            ['noGender', 'dat', 'sing'],
                            ['masc', 'dat', 'sing'],
                            ['noGender', 'nom', 'sing'],
                            ['masc', 'nom', 'sing'],
                            ['noGender', 'acc', 'sing']]}
    """

    gender = ["masc", "fem", "neut"]  # +'noGender' - ?
    case = ["nom", "acc", "dat", "gen"]
    number = ["sing", "plu"]

    allowed_pos = ["ART", "ADJ", "DEMO", "POS", "NN", "NP", "NE"]

    np_morph_filtered = {}
    for token, values_list in np_morph.items():
        unique_values = []
        for values in values_list:
            # POS filter
            if values[0].split()[1] in allowed_pos:
                pos = values[0].split()[1]
                # gender/case/number filter
                filtered_values = [pos] + [
                    v for v in values if v in gender or v in case or v in number
                ]
                # "lower than 3 attributes" and uniqueness filters
                if len(filtered_values) >= 4 and filtered_values not in unique_values:
                    unique_values.append(filtered_values)
        np_morph_filtered[token] = unique_values

    return np_morph_filtered


def save_congruency_results(congruency_results: dict) -> None:
    """
    Die Ergebnisse der Auswertung speichern

    Args:
        congruency_results

         Die Auswertung der Kongruenz der NPs

    Returns:
        None

    """
    with open("main_results.csv", mode="w", encoding="utf-8") as save:
        csv_writer = csv.writer(save, delimiter=",")

        for np in congruency_results:

            case = congruency_results.get(np)[-2]
            demorphy = congruency_results.get(np)[:-2]
            congruency = congruency_results.get(np)[-1]

            results = (np, case, demorphy, congruency)

            csv_writer.writerow(results)

    return congruency_results


if __name__ == "__main__":

    pass
