# Standard
# None

# Pip
# None

# Custom
from kongru.api_general.universal.constants.general_paths import GeneralPaths as Gp
from kongru.api_general.universal.funcs.general_tools import (
    find_np_morphology,
)
from kongru.api_general.universal.funcs.basic_readers import (
    read_in_np_file,
    read_morpho_dict,
)

from kongru.api_general.universal.funcs.basic_savers import save_congruency_results


def np_congruency(morpho_results, np, np_article, article_codes):

    try:
        case = morpho_results.get("case").strip()
        np_data = morpho_results.get("np_data")
        tagged_data = dict()

        for row in np_data:
            # Leerzeilen nicht beachten
            split_data = [data for data in row.split(" ") if data]

            if len(split_data) == 2:
                word, tag = split_data
                tagged_data[tag] = word

        # DET and ADJ
        head = tagged_data.get("NN")
        article = tagged_data.get("DET", "ART")
        adj = tagged_data.get("ADJ")
        gender = morpho_results.get(head)[0][1]
        gender_code = np_article.get(gender).index(article)
        check_gender = bool(np_article.get(gender)[gender_code])

        # Genus und Kasus
        # Nom und Akk sind gleich, deswegen wird der Zeiger verschoben
        if gender == "fem" or "neut":
            check_case = article_codes.get(gender_code)
            if not check_case:
                move = 1
                check_case = article_codes.get(gender_code + move) == case
        else:
            check_case = article_codes.get(gender_code) == case

        check_adjective = False

        if adj:
            for row in morpho_results.get(adj):

                if gender in row and case in row:
                    check_adjective = True
        else:
            check_adjective = True

        checks = {"ADJ": check_adjective, "gender": check_gender, "case": check_case}

        correct_checks = 0

        for check in checks:
            value = checks.get(check)
            if value:
                correct_checks += 1

        if correct_checks == len(checks):
            np_data.append(1)
            return np_data
        else:
            np_data.append(0)
            return np_data

    except Exception as e:
        np_data.append(99)
        return np_data


def determine_congruency(morpho_results: dict[list, str]):
    """
    Hier soll die einfache Kongruenz der jeweiligen NPs bestimmt werden.

    Args:
        morpho_results (dict[str,dict]): Die Saetze mit deren zugehoerigen
          morphologische Information.

        z.B.
        {'Der kleiner Hund': {'Der': 'ART,M,SING,NOM',
        'kleiner': 'ADJ,M',
        'Hund': 'NOUN,M,SING,NOM'},
      'Das kleiner Hund': {'Das': 'ART,N,SING,NOM',
        'kleiner': 'ADJ,M',
        'Hund': 'NOUN,M,SING,NOM'}}

    Returns:
        congruency_reslts(dict[list, tuple[str | Any, int] | tuple[str, int]):
    Die Auswertung der Kongruenz der NPs
    """
    congruency_results = dict()

    # nom, akk, dativ, gentiv
    np_article = {
        "masc": ["der", "den", "dem", "des"],
        "fem": ["die", "die", "der", "der"],
        "neut": ["das", "das", "dem", "des"],
        "plural": ["die", "die", "den", "der"],
    }
    article_codes = {0: "nom", 1: "acc", 2: "dat", 3: "gen"}

    for np in morpho_results:

        # Die NP wird nur analysiert, wenn die NP-Konstinuente in Demorphy
        # vorkommen.
        np_info = morpho_results.get(np)

        if np_info:
            result = np_congruency(np_info, np, np_article, article_codes)
            congruency_results[np] = result

    return congruency_results


def run_quick_analysis(
    np_file: str = Gp.TEST_NP_FILE.value,
    morpho_dict_file: str = Gp.DB_DEMORPHY_TXT.value,
) -> None:
    """

    :param
        np_file:
        morpho_dict_file:
    :return
        None
    """
    try:
        # Die einzulesenden Dateien
        np_data = read_in_np_file(np_file)

        morpho_dict_data = read_morpho_dict(morpho_dict_file, use_pickle_file=True)

        # NP tokenisieren und Kongruenz bestimmen
        tok_morph_np = find_np_morphology(morph_dict=morpho_dict_data, np_data=np_data)
        np_congruency = determine_congruency(tok_morph_np)
        print(np_congruency)
        # Ergebnisse speichern
        save_congruency_results(np_congruency)
        print("Ergebnisse wurden gespeichert.")

        # Fuer die Unnit Tests Relevant
        return True

    except Exception as e:
        print(e)
        return e


if __name__ == "__main__":
    run_quick_analysis()
