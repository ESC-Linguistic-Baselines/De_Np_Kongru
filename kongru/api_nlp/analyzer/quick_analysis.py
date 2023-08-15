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
from kongru.api_nlp.analyzer.np_congruency import determine_congruency


def run_quick_analysis(
    np_file: str = Gp.NP_FILE.value, morpho_dict_file: str = Gp.DEMORPHY_DICT.value
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
