# Standard
# None

# Pip
import typer

# Custom

# api_general

# const
from kongru.api_general.universal.constants.general_paths import GeneralPaths as Gp

# funcs
from kongru.api_general.universal.funcs.basic_logger import (
    catch_and_log_error,
    log_info,
)
from kongru.api_nlp.congruential_analysis.analyzers.demorphy_analyzer import (
    DemorphyAnalyzer,
)

# api_nlp

from kongru.api_nlp.congruential_analysis.congruency.nominal_phrase_congruency import (
    NominalPhraseCongruency,
)

app_typer_congruential_analysis = typer.Typer(
    name="kongruenz",
    help="Die NP-Eintraege auswerten",
    add_help_option=False,
    no_args_is_help=True,
)


@app_typer_congruential_analysis.command(
    name = "np_analyse",
    help= "Die Kongruenz der Nps in einer datei bestimmen "
)
def nominal_phrase_agreement_analysis(
    file_name: str = typer.Argument(
        default=Gp.TEST_NP_FILE_CSV.value,
        help="",
    ),
    save_results: bool = typer.Argument(default=True, help="Ergebnisse speichern"),
) -> None:
    """ """
    try:
        # Die einzulesenden Dateien
        demorphy = DemorphyAnalyzer()
        demorphy.file_name = file_name

        # Morphologische Ergebnisse
        morpho_results = demorphy.get_raw_np_morphology()

        # Kongruenz bestimmen
        np_congruency = NominalPhraseCongruency(
            morpho_results=morpho_results, save_file_name="np_test_1023_0001416.csv"
        )

        # Ergebnisse speichern
        if save_results:
            pass
            np_congruency.save_congruency_results()
            log_info(msg="Ergebnisse wurden gespeichert", echo_msg=True)
        else:
            typer.echo(np_congruency)
    except Exception as e:
        catch_and_log_error(
            error=e, custom_message="Bei der Analyse ist etwas schief gelaufen."
        )


if __name__ == "__main__":
    app_typer_congruential_analysis()
