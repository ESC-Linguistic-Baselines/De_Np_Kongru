# Standard
import os

# Pip
import typer

# Custom
# api_general
# managers
from kongru.api_general.database_managers.managers.merlin_manager import (
    MerlinManager as Merlin,
)
from kongru.api_general.database_managers.extractors.ast_nominal_phrase_extractor import (
    AstNominalPhraseExtractor,
)

# Funcs
from kongru.api_general.universal.funcs.basic_logger import (
    catch_and_log_error,
    log_info,
)
from kongru.api_general.universal.funcs.natural_order_group import NaturalOrderGroup

# constants
from kongru.api_general.universal.constants.general_paths import GeneralPaths as Gp

app_typer_data_managers = typer.Typer(
    no_args_is_help=True,
    name="datenbank",
    help="Die Datenbankcorpora verwalten und durchsuchen",
    add_completion=False,
    cls=NaturalOrderGroup,
)


@app_typer_data_managers.command(name="text_ids", help="Ids der Textdateien auflisten")
def list_text_ids() -> None:
    sql = "SELECT general_author_id FROM learner_text_data"
    text_ids = Merlin(sql_command=sql).read_database()
    for row in text_ids:
        typer.echo(*row)


@app_typer_data_managers.command(name="text_lesen", help="einen bestimmten Text lesen")
def look_up_text_by_id(
    text_id: str = typer.Option(
        "1031_0003130",
        "--text_id",
        "--id",
        help="Die Text-Id des gewuenschten Textes angeben",
    )
):
    merlin_corpus = Merlin(text_id=text_id).extract_entry_by_id()
    custom_message = "Die Text-ID, die eingegeben wurde, ist nicht gültig."

    if merlin_corpus:
        merlin_corpus.pop("conll")
        try:
            # Die CONLL-Info ist zu viel, daher wird sie entfernt.
            for entry in merlin_corpus:
                print(entry, merlin_corpus.get(entry))
        except Exception as e:

            catch_and_log_error(error=e, custom_message=custom_message)
    else:
        log_info(
            msg=custom_message,
            echo_msg=True,
            log_error=False,
            echo_color=typer.colors.RED,
        )


@app_typer_data_managers.command(name="np_lesen")
def read_np_file():
    pass


@app_typer_data_managers.command(name="daten_extrahieren")
def extract_data_from_merlin_database():
    with open(Gp.SQL_MERLIN.value, "r") as sql_file:
        sql_script = sql_file.read()

    text_ids = Merlin(sql_command=sql_script).read_database()
    for row in text_ids:
        pass


@app_typer_data_managers.command(
    name="nps_extrahieren", help="Nps aus einer bestimmen Datei lesen"
)
def extract_nps(
    file_name: str = typer.Option(
        default=Gp.TEST_NP_AST_FILE.value,
        help="Der Name der Ast-Datei, die ausgewertet werden soll.",
    ),
):
    base_file_name = os.path.basename(file_name)
    file, extension = base_file_name.split(".")

    np_file_handler = AstNominalPhraseExtractor(
        file_name=file_name, save_name=f"{Gp.RES_AST_NP_FILE.value}_{file}.csv"
    )
    np_file_handler.save_extracted_ast_nps()

    typer.secho(
        message="Ast-Datei wurde ausgelesen und gespeichert.", fg=typer.colors.GREEN
    )


@app_typer_data_managers.command(name="json_erstellen")
def create_np_json_file():
    pass


@app_typer_data_managers.command(name="conll_erstellen")
def create_conoll_file():
    pass


@app_typer_data_managers.command(name="np_zu_json")
def add_np_results_to_np_json_file():
    pass


if __name__ == "__main__":
    extract_data_from_merlin_database()
