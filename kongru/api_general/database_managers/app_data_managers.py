# Standard
import os

# Pip
import typer

from rich.console import Console
from rich.table import Table

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
    catch_and_log_info,
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

console = Console()


@app_typer_data_managers.command(name="text_ids", help="Ids der Textdateien auflisten")
def show_text_ids() -> None:
    sql_command = "SELECT general_author_id,general_mother_tongue,general_cefr," \
          "txt_len_in_char FROM learner_text_data "
    text_ids = Merlin(sql_command=sql_command).read_database()
    table = Table("general_author_id", 'general_mother_tongue', "general_cefr",
                  "txt_len_in_char")
    for id_entry in sorted(text_ids):
        table.add_row(*id_entry)
    console.print(table)


@app_typer_data_managers.command(name="text_lesen",
                                 help="einen bestimmten Text in der Datenbank lesen")
def get_and_show_text_by_id(
    text_id: str = typer.Option(
        "1031_0003130",
        "--text_id",
        "--id",
        help="Die Text-Id des gewuenschten Textes angeben",
    )
) -> None:
    entries_extracted_by_text_id = Merlin(text_id=text_id).extract_entry_by_id()
    custom_message = "Die Text-ID, die eingegeben wurde, ist nicht gültig."

    # Nur wenn ein Eintrag vorhanden ist
    if entries_extracted_by_text_id:

        # Die CONLL-Info ist zu viel, daher wird sie entfernt.
        entries_extracted_by_text_id.pop("conll")
        try:
            for entry in entries_extracted_by_text_id:
                typer.echo(f"{entry} {entries_extracted_by_text_id.get(entry)}")
        except Exception as e:
            catch_and_log_error(error=e,
                                custom_message=custom_message)
    else:
        catch_and_log_info(
            msg=custom_message,
            echo_msg=True,
            log_info_message=False,
            echo_color=typer.colors.RED,
        )


@app_typer_data_managers.command(name="nps_lesen",
                                 help="Nps aus einer bestimmten Datei lesen")
def read_np_file(
        file_type: str = typer.Option(
          "ast",
            "--datei_typ",
            "--typ"
        ),
        data_source: bool = typer.Option(
            True,
            "--datenbank",
            "--eingangsdatei"
        )
) -> None :

    if file_type == "ast":
        pass
    if file_type == "conll":
        pass
    if file_type == "full_json":
        pass
    if file_type == "pylist":
        pass
    if file_type == "raw":
        pass


@app_typer_data_managers.command(name="daten_extrahieren")
def extract_data_from_merlin_database():
    with open(Gp.SQL_MERLIN.value, "r") as sql_file:
        sql_script = sql_file.read()
    text_ids = Merlin(sql_command=sql_script).read_database()
    for row in text_ids:
        print(row)


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
