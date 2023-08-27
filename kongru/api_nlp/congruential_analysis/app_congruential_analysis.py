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
from kongru.api_general.universal.funcs.basic_logger import catch_and_log_error
from kongru.api_nlp.congruential_analysis.analyzers.demorphy_analyzer import (
    DemorphyAnalyzer,
)

# api_nlp

from kongru.api_nlp.congruential_analysis.congruency.np_congruency import \
    NominalPhraseCongruency

app_typer_congruential_analysis = typer.Typer(
    name="kongruenzanalyse",
    help="Die NP-Eintraege auswerten",
    add_help_option=False,
    no_args_is_help=True,
)


@app_typer_congruential_analysis.command()
def run_analysis(file_name: str = typer.Argument(default="/Users/christopherchandler/repo/Python/De_NP_Kongru/user/outgoing/np/np_test_1023_0001416.csv",
                                                 help=""),
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
        np_congruency = NominalPhraseCongruency(morpho_results=morpho_results,
                                                save_file_name= "np_test_1023_0001416.csv")

        # Ergebnisse speichern
        if save_results:
            pass
            np_congruency.save_congruency_results()
            #typer.echo("Ergebnisse wurden gespeichert.")
        else:
            typer.echo(np_congruency)
    except Exception as e:
        catch_and_log_error(
            error=e,
            custom_message="Bei der Analyse ist etwas schief gelaufen."
        )

if __name__ == "__main__":
    app_typer_congruential_analysis()
