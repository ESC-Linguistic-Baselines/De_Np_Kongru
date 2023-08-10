import pickle
import ast


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

    return morph_dict
