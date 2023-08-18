# Standard
# None

# Pip
import typer

from deprecate.basic_savers import save_congruency_results
# Custom

# api_general

# const
from kongru.api_general.universal.constants.general_paths import GeneralPaths as Gp

# parsers
# None

# funcs

from kongru.api_general.universal.funcs.basic_logger import get_logger
from kongru.api_nlp.congruential_analysis.analyzers.demorphy_analyzer import (
    DemorphyAnalyzer,
)

# api_nlp

from kongru.api_nlp.congruential_analysis.congruency.np_congruency import NpCongruency

app_typer_congruential_analysis = typer.Typer(
    name="kongruenzanalyse",
    help="Die NP-Eintraege auswerten",
    add_help_option=False,
    no_args_is_help=True,
)


@app_typer_congruential_analysis.command()
def run_simple_analysis() -> None:
    """
    :param
        np_file:
        morpho_dict_file:
    :return
        None
    """
    try:
        demorphy = DemorphyAnalyzer(word="")

        # Die einzulesenden Dateien
        morpho_results = demorphy.find_raw_np_morphology()
        np_congruency = NpCongruency(morpho_results=morpho_results).check_congruency()

        # Ergebnisse speichern
        save_congruency_results(np_congruency)
        print("Ergebnisse wurden gespeichert.")

    except Exception as e:
        logger = get_logger()
        custom_message = "Die Analyse konnte nicht durchgefuehrt werden."
        logger.error(e, extra={"custom_message": custom_message})
        typer.echo(custom_message)
        typer.echo(e)


if __name__ == "__main__":
    app_typer_congruential_analysis()
