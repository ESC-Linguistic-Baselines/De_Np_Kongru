# Standard
import ast
import csv
import pickle

# Pip
# None

# Custom
from typing import Any


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
            print(token, values_list)
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


if __name__ == "__main__":

    pass
