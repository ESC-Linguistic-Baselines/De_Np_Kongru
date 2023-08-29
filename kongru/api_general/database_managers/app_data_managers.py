# Standard
# None

# Pip
import typer

# Custom
# api_general
# managers
from kongru.api_general.database_managers.managers.merlin_manager import (
    MerlinManager as Merlin,
)
from kongru.api_general.database_managers.extractors import ast_nominal_phrase_extractor

# Funcs
from kongru.api_general.universal.funcs.basic_logger import catch_and_log_error, \
    log_info

# constas
from kongru.api_general.universal.constants.general_paths import GeneralPaths as Gp

app_typer_data_managers = typer.Typer(
    no_args_is_help=True,
    name="datenbank",
    help="Die Datenbankcorpora verwalten und durchsuchen",
    add_completion=False,
)


# Merlin Parser
@app_typer_data_managers.command(
    name="text_eintrag", help="nach einem bestimmten Text suchen"
)
def look_up_data_entry(
    text_id: str = typer.Argument(
        "1031_0003130", help="Die Text-Id des gewuenschten Textes angeben"
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

            catch_and_log_error(
                 error=e,
                 custom_message=custom_message
             )
    else:
        log_info(
            msg=custom_message,
            echo_msg=True,
            log_error=False,
            echo_color=typer.colors.RED
        )

@app_typer_data_managers.command(
    name="ast_datei_lesen", help="Eine bestimmte Ast-Datei inspezieren"
)
def view_ast_file(
    file_name: str = typer.Argument(
        default=Gp.TEST_NP_AST_FILE.value,
        help="Der Name der Ast-Datei, die ausgelesen werden soll."
    )
):
    AutoAnnotation(file_name).run_auto_annotation()


@app_typer_data_managers.command(
    name="ast_datei_nps", help="Nps aus einer bestimmten Ast-Datei lesen"
)
def extract_nps_from_ast_file(
    file_name: str = typer.Argument(
        default="", help="Der Name der Ast-Datei, die ausgewertet werden soll."
    )
):
    np_file_handler = ast_nominal_phrase_extractor(file_name=file_name)
    np_file_handler.save_extracted_ast_nps()
    typer.secho(message="Ast-Datei wurde ausgelesen", fg=typer.colors.GREEN)


if __name__ == "__main__":
    app_typer_data_managers()
