# Standard
# None

# Pip
# None

# Custom
from dp_np_kongru.constants.general_paths import GeneralPaths as Gp
from dp_np_kongru.utils.kongruenz import run_congruency_check
from dp_np_kongru.utils.savers import save_congruency_results


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
    # Kongruenzkontroll durchfuehren
    np_congruency_results = run_congruency_check(np_file, morpho_dict_file)

    # Ergebnisse speichern
    save_congruency_results(np_congruency_results)


if __name__ == "__main__":
    pass
