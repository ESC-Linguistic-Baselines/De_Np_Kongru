# Standard
# None

# Pip
import typer

from rich.console import Console
from rich.table import Table

# Custom

# api_general

# const
from kongru.api_general.universal.constants.general_paths import GeneralPaths as Gp

# funcs
from kongru.api_general.universal.funcs.basic_logger import (
    catch_and_log_error,
    catch_and_log_info,
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

# Konsole zur Erstellung einer Tabelle
console = Console()


@app_typer_congruential_analysis.command(
    name="np_analyse", help="Die Kongruenz der Nps in einer datei bestimmen "
)
def nominal_phrase_agreement_analysis(
    file_name: str = typer.Option(
        Gp.TEST_NP_FILE_CSV.value,
        "--datei_name",
        "--d",
        help="Die NP-datei, die ausgewertet werden soll.",
    ),
    save_results: bool = typer.Option(
        True, "--speichern", "--anzeigen", help="Ergebnisse speichern"
    ),
    save_file: str = typer.Option(
        "np.csv",
        "--speichern-ergebnisse",
        "--speichern",
        help="Der Name des Ergebnisse ",
    ),
) -> None:
    """ """
    try:
        # Demorphy aufstellen, um die Datei auswerten zu koennen
        demorphy = DemorphyAnalyzer()
        demorphy.file_name = file_name

        # Morphologische Ergebnisse
        morpho_results = demorphy.get_raw_np_morphology()

        # Kongruenz bestimmen
        np_congruency = NominalPhraseCongruency(
            file_name=file_name, morpho_results=morpho_results, save_file_name=save_file
        )

        # Ergebnisse speichern
        if save_results:
            # Die Ergebnisse werden zwar gespeichert, aber nicht angezeigt.
            np_congruency.save_congruency_results()
            catch_and_log_info(
                msg="Die Ergebnisse der Auswertung wurden gespeichert.",
                echo_msg=True,
            )
        else:
            # Die Ergebnisse werden zwar angezeigt, aber nicht gespeichert
            congruency_check = np_congruency.run_congruency_check()
            table = Table("Status", "Nominal Phrase")
            for entry in congruency_check:
                data = congruency_check.get(entry)
                status, nominal_phrase = data[:2]
                table.add_row(status, nominal_phrase)
            console.print(table)

    except Exception as e:
        catch_and_log_error(
            error=e, custom_message="Bei der Analyse ist etwas schief gelaufen."
        )


if __name__ == "__main__":
    app_typer_congruential_analysis()
