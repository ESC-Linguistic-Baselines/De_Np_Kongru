# Standard
# None

# Pip
import typer

from kongru.api_general.data_parsers.demorphy_parser import DemorphyParser
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

from deprecate.basic_savers import save_congruency_results

# api_nlp

from kongru.api_nlp.congruential_analysis.congruency.np_congruency import NpCongruency

app_typer_congruential_analysis = typer.Typer(
    name="kongruenzanalyse",
    help="Die NP-Eintraege auswerten",
    add_help_option=False,
    no_args_is_help=True,
)


@app_typer_congruential_analysis.command()
def run_analysis(file_name: str = typer.Argument(default="/Users/christopherchandler/"
                                                         "repo/Python/De_NP_Kongru/user/"
                                                         "outgoing/np/test_np_file.csv"),
        save_results: bool = typer.Argument(default=True,
                                                     help="Ergebnisse speichern")
                 ) -> None:
    """

    """
    try:
        # Die einzulesenden Dateien
        demorphy = DemorphyAnalyzer()
        demorphy.file_name = file_name

        # Morphologische Ergebnisse
        morpho_results = demorphy.find_raw_np_morphology()

        # Kongruenz bestimmen
        np_congruency = NpCongruency(morpho_results=morpho_results)
        check_congruency = np_congruency.check_congruency()

        # Ergebnisse speichern
        if save_results:
            np_congruency.save_congruency_results(check_congruency)
            typer.echo("Ergebnisse wurden gespeichert.")
        else:
            typer.echo(np_congruency)

    except Exception as e:
        logger = get_logger()
        custom_message = "Die Analyse konnte nicht durchgefuehrt werden."
        logger.error(e, extra={"custom_message": custom_message})
        typer.echo(custom_message)
        typer.echo(e)


if __name__ == "__main__":
    app_typer_congruential_analysis()
