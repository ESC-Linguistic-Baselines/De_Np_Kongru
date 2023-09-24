# Standard
# None
import glob
import time

# Pip
import typer

from rich.console import Console
from rich.table import Table

# Custom

# api_general

# const
from kongru.api_general.universal.constants.general_paths import GeneralPaths as Gp

# funcs
from kongru.api_general.universal.funcs import (
    basic_logger,
    get_ast_data,
    get_np_data,
    get_np_results,
    json_creator,
)

from kongru.api_general.universal.constants.message_keys import MessageKeys as Mk
from kongru.api_general.universal.funcs.natural_order_group import NaturalOrderGroup

# api_nlp
from kongru.api_nlp.congruential_analysis.analyzers.demorphy_analyzer import (
    DemorphyAnalyzer,
)

from kongru.api_nlp.congruential_analysis.congruency.nominal_phrase_congruency import (
    NominalPhraseCongruency,
)
from kongru.api_nlp.congruential_analysis.congruency.multi_np_analysis import (
    generate_results_file,
)

from kongru.api_nlp.congruential_analysis.congruency.run_congruency_algorithm import (
    run_batch_congruency,
)


from kongru.api_general.database_managers.managers.merlin_manager import MerlinManager

merlin = MerlinManager()

congruential_keys = Mk.AppCongruentialAnalysis
general_keys = Mk.General

app_typer_congruential_analysis = typer.Typer(
    name=congruential_keys.APP_NAME.value,
    help=congruential_keys.APP_NAME_HELP.value,
    add_help_option=True,
    no_args_is_help=True,
    cls=NaturalOrderGroup,
)

# Konsole zur Erstellung einer Tabelle
console = Console()


@app_typer_congruential_analysis.command(
    name=congruential_keys.NP_AGREEMENT_SINGULAR_NAME.value,
    help=congruential_keys.NP_AGREEMENT_SINGULAR_HELP.value,
)
def singular_nominal_phrase_agreement_analysis(
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
        help=general_keys.SAVE_RESULTS_HELP.value,
    ),
) -> None:
    """
    Analysiere die Kongruenz in nominalen Phrasen in einer gegebenen CSV-Datei.

    Args: file_name (str): Der Name der CSV-Datei mit den Daten zur Analyse.
    save_results (bool): Ob die Analyseergebnisse in einer CSV-Datei gespeichert
    werden sollen. save_file (str): Der Name der CSV-Datei, in die die Ergebnisse
    gespeichert werden sollen.

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

            basic_logger.catch_and_log_info(
                custom_message=congruential_keys.NP_AGREEMENT_SAVE.value,
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
        basic_logger.catch_and_log_error(
            error=e, custom_message=congruential_keys.NP_AGREEMENT_ERR.value
        )


@app_typer_congruential_analysis.command(
    name=congruential_keys.NP_AGREEMENT_MULTI_NAME.value,
    help=congruential_keys.NP_AGREEMENT_MULTI_HELP.value,
)
def multi_nominal_phrase_agreement_analysis(
    text_amount: int = typer.Option(
        congruential_keys.MULTI_AGREEMENT_AMOUNT_DEFAULT.value,
        congruential_keys.MULTI_AGREEMENT_AMOUNT_LONG.value,
        congruential_keys.MULTI_AGREEMENT_AMOUNT_SHORT.value,
        help=congruential_keys.MULTI_AGREEMENT_AMOUNT_HELP.value,
    ),
    text_id_sources: str = typer.Option(
        Gp.NP_TRAINING_IDS.value,
        congruential_keys.MULTI_AGREEMENT_ID_SOURCE_LONG.value,
        congruential_keys.MULTI_AGREEMENT_ID_SOURCE_SHORT.value,
        help=congruential_keys.MULTI_AGREEMENT_ID_SOURCE_HELP.value,
    ),
) -> None:
    """

    Args:
        text_amount:
        text_id_sources:

    Returns:
        None

    """
    # Dateien aufstellen
    file_ids = open(text_id_sources, mode="r", encoding="utf-8").readlines()

    text_id_numbers = [file.strip() for file in file_ids]
    np_extracted_files = glob.glob(Gp.NP_EXTRACTED_FILES_GLOB.value)
    np_res_files = glob.glob(Gp.NP_CSV_RES_FILES_GLOB.value)

    # Time, damit die Dateien zeitlich erfasst werden.
    get_ast_data.ast_data()
    time.sleep(0.500)
    get_np_data.np_data()

    # Kongruenz fuer mehrere Dateien durchfuehren
    run_batch_congruency(
        congruency_algo=singular_nominal_phrase_agreement_analysis,
        np_files=np_extracted_files,
        text_id_numbers=text_id_numbers,
        text_limit=text_amount,
    )

    time.sleep(0.500)
    count_results = get_np_results.count_np_results(np_res_files)
    time.sleep(0.500)
    generate_results_file(count_results)
    time.sleep(0.500)

    typer.echo("....json Dateien generieren")
    json_creator.generate_np_json_files(text_id_numbers)

    typer.echo(".json und .csv Ergebnisse zusammenfuehren")
    json_creator.combine_csv_json_data()
    typer.echo(".json und .csv Ergebnisse erfolgreich zusammengefuehrt worden.")


if __name__ == "__main__":
    app_typer_congruential_analysis()
