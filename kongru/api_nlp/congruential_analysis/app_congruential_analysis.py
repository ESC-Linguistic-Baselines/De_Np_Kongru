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

from kongru.api_general.universal.constants.message_keys import MessageKeys as Mk

congruential_keys = Mk.AppCongruentialAnalysis
general_keys = Mk.General

app_typer_congruential_analysis = typer.Typer(
    name=congruential_keys.APP_NAME.value,
    help=congruential_keys.APP_NAME_HELP.value,
    add_help_option=True,
    no_args_is_help=True
)

# Konsole zur Erstellung einer Tabelle
console = Console()


@app_typer_congruential_analysis.command(
    name=congruential_keys.NP_AGREEMENT_NAME.value,
    help=congruential_keys.NP_AGREEMENT_HELP.value,
)
def nominal_phrase_agreement_analysis(
    file_name: str = typer.Option(
        Gp.TEST_NP_FILE_CSV.value,
        general_keys.FILE_NAME_LONG.value,
        general_keys.FILE_NAME_SHORT.value,
        help=general_keys.FILE_NAME_HELP.value,
    ),
    save_results: bool = typer.Option(
        congruential_keys.NP_AGEREMENT_SAVE_DEFAULT.value,
        congruential_keys.NP_AGREEMENT_SAVE_TRUE.value,
        congruential_keys.NP_AGREEMENT_SAVE_FALSE.value,
        help=congruential_keys.NP_AGREEMENT_SAVE_HELP.value,
    ),
    save_file: str = typer.Option(
        general_keys.SAVE_DEFAULT_CSV.value,
        general_keys.SAVE_RESULTS_LONG.value,
        general_keys.SAVE_DIR_SHORT.value,
        help=general_keys.SAVE_FILE_HELP.value,
    )
) -> None:
    """
    Analysiere die Kongruenz in nominalen Phrasen in einer gegebenen CSV-Datei.

    Args:
        file_name (str): Der Name der CSV-Datei mit den Daten zur Analyse.
        save_results (bool): Ob die Analyseergebnisse in einer CSV-Datei gespeichert werden sollen.
        save_file (str): Der Name der CSV-Datei, in die die Ergebnisse gespeichert werden sollen.

    Returns:
        None
    """

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
                msg=congruential_keys.NP_AGREEMENT_SAVE.value,
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
            error=e, custom_message=congruential_keys.NP_AGREEMENT_ERR.value
        )


if __name__ == "__main__":
    app_typer_congruential_analysis()
