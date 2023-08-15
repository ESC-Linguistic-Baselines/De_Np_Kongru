# Standard
import csv

# Pip
# None

# Custom
from kongru.api_general.constants.general_paths import GeneralPaths as Gp
from kongru.api_general.constants.general_vars import TIMESTAMP


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
        f"{Gp.SAVE_DIRECTORY_NP.value}/{TIMESTAMP}_quick_results.csv",
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

            # e.g.  der Hund (whole NP) + der ART, Hund N (tokens) + nom (required case)
            result = [" ".join(pure_NP)] + tokens + [case]

            csv_writer.writerow([", ".join(result)])

    return None
