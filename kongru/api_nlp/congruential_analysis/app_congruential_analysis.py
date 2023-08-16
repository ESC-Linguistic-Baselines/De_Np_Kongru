# Standard
# None

# Pip
import typer

# Custom

# api_general

# const
from kongru.api_general.universal.constants.general_paths import GeneralPaths as Gp

# parsers
from kongru.api_general.data_parsers.demorphy_parser import DemorphyParser

# funcs
from kongru.api_general.universal.funcs.general_tools import find_np_morphology

from kongru.api_general.universal.funcs.basic_readers import (
    read_in_np_file,
    read_morpho_dict,
)
from kongru.api_general.universal.funcs.basic_savers import (
    save_congruency_results,
)
from kongru.api_general.universal.funcs.basic_logger import get_logger

# api_nlp
from kongru.api_nlp.congruential_analysis.congruency.np_congru_runner import (
    run_congruency_checker,
)


app_typer_congruential_analysis = typer.Typer(
    name="kongruenzanalyse",
    help="Die NP-Eintraege auswerten",
    add_help_option=False,
    no_args_is_help=True,
)


@app_typer_congruential_analysis.command()
def run_simple_analysis(
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
        demorphy_parser = DemorphyParser()
        # Die einzulesenden Dateien
        np_data = read_in_np_file(np_file)

        morpho_dict_data = read_morpho_dict(morpho_dict_file, use_pickle_file=True)

        # NP tokenisieren und Kongruenz bestimmen
        tok_morph_np = find_np_morphology(morph_dict=morpho_dict_data, np_data=np_data)
        np_congruency = run_congruency_checker(tok_morph_np)
        print(np_congruency)
        # Ergebnisse speichern
        save_congruency_results(np_congruency)
        print("Ergebnisse wurden gespeichert.")

    except Exception as e:
        logger = get_logger()
        custom_message = "Die Analyse konnte nicht durchgefuehrt werden."
        logger.error(e, extra={"custom_message": custom_message})


if __name__ == "__main__":
    app_typer_congruential_analysis()
