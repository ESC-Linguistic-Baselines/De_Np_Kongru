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


# Merlin Parser
@app_typer_data_managers.command(
    name="text_eintrag", help="einen bestimmten Text aufrufen"
)
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


@app_typer_data_managers.command(
    name="ast_datei_lesen", help="Eine bestimmte Ast-Datei inspezieren"
)
def view_ast_file(
    file_name: str = typer.Option(
        default=Gp.TEST_NP_AST_FILE.value,
        help="Der Name der Ast-Datei, die ausgelesen werden soll.",
    )
):
    pass


@app_typer_data_managers.command(
    name="ast_datei_nps", help="Nps aus einer bestimmten Ast-Datei lesen"
)
def extract_nps_from_ast_file(
    file_name: str = typer.Option(
        default=Gp.TEST_NP_AST_FILE.value,
        help="Der Name der Ast-Datei, die ausgewertet werden soll.",
    ),
):
    base_file_name = os.path.basename(file_name)
    file, extension = base_file_name.split(".")

    print(f"{Gp.RES_AST_NP_FILE.value}_{file}.csv")
    np_file_handler = AstNominalPhraseExtractor(
        file_name=file_name, save_name=f"{Gp.RES_AST_NP_FILE.value}_{file}.csv"
    )
    np_file_handler.save_extracted_ast_nps()

    typer.secho(
        message="Ast-Datei wurde ausgelesen und gespeichert.", fg=typer.colors.GREEN
    )


if __name__ == "__main__":
    app_typer_data_managers()
