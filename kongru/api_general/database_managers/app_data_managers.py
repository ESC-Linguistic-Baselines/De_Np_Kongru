# Standard
import os
import time

# Pip
from tqdm import tqdm
import typer

from rich.console import Console
from rich.table import Table

# Custom

# extractors
from kongru.api_general.database_managers.extractors.extract_conll_to_pylist import (
    main_conll_to_pylist,
)

# managers
from kongru.api_general.database_managers.managers.merlin_manager import (
    MerlinManager as Merlin,
)
from kongru.api_general.database_managers.extractors.ast_nominal_phrase_extractor import (
    AstNominalPhraseExtractor,
)

# funcs
from kongru.api_general.universal.funcs.basic_logger import (
    catch_and_log_error,
    catch_and_log_info,
)
from kongru.api_general.universal.funcs.natural_order_group import NaturalOrderGroup

# constants
from kongru.api_general.universal.constants.general_paths import GeneralPaths as Gp
from kongru.api_general.universal.constants.message_keys import MessageKeys as Mk


# Strings als Enums
manager_keys = Mk.AppDataManager
general_keys = Mk.General
merlin_keys = Mk.Merlin


app_typer_data_managers = typer.Typer(
    no_args_is_help=True,
    name=manager_keys.APP_NAME.value,
    help=manager_keys.APP_NAME_HELP.value,
    add_completion=False,
    cls=NaturalOrderGroup,
)

console = Console()


@app_typer_data_managers.command(
    name=manager_keys.SHOW_TEXT_IDS_COMMAND_NAME.value,
    help=manager_keys.SHOW_TEXT_IDS_COMMAND_HELP.value,
)
def show_text_ids() -> None:
    """
    Zeigt die Text-IDs an.

    Diese Funktion ruft die Text-IDs aus der Merlin-Korpus-Datenbank ab
    und zeigt sie in einer Tabelle an.

    Returns:
        None
    """
    sql_command = manager_keys.SHOW_TEXT_IDS_SQL_COMMAND.value

    text_ids = Merlin(sql_command=sql_command).read_merlin_corpus_database()
    table = Table(manager_keys.SHOW_TEXT_IDS_COMMAND_NAME.value)
    for id_entry in sorted(text_ids):
        table.add_row(*id_entry)
    console.print(table)


@app_typer_data_managers.command(
    name=manager_keys.GET_AND_SHOW_TEXT_BY_ID_NAME.value,
    help=manager_keys.GET_AND_SHOW_TEXT_BY_ID_HELP.value,
)
def get_and_show_text_by_id(
    text_id: str = typer.Option(
        manager_keys.GET_AND_SHOW_TEXT_BY_ID_TEXT_ID_DEFAULT.value,
        manager_keys.GET_AND_SHOW_TEXT_BY_ID_TEXT_ID_LONG.value,
        manager_keys.GET_AND_SHOW_TEXT_BY_ID_TEXT_ID_SHORT.value,
        help=manager_keys.GET_AND_SHOW_TEXT_BY_ID_TEXT_ID_HELP.value,
    )
) -> None:
    """
    Zeigt den Text anhand seiner ID an.

    Diese Funktion zeigt den Text an, der mit der angegebenen Text-ID in Verbindung steht.

    Args:
        text_id (str): Die ID des anzuzeigenden Texts.

    Returns:
        None
    """
    entries_extracted_by_text_id = Merlin(
        merlin_txt_id=text_id
    ).extract_merlin_corpus_entry_by_id()

    # Nur wenn ein Eintrag vorhanden ist
    if entries_extracted_by_text_id:

        # Die CONLL-Info ist zu viel, daher wird sie entfernt.
        entries_extracted_by_text_id.pop("conll")
        try:
            for entry in entries_extracted_by_text_id:
                typer.echo(f"{entry} {entries_extracted_by_text_id.get(entry)}")
        except Exception as e:
            catch_and_log_error(
                error=e, custom_message=merlin_keys.INVALID_TEXT_ID.value
            )
    else:
        catch_and_log_info(
            custom_message=merlin_keys.INVALID_TEXT_ID.value,
            echo_msg=True,
            log_info_message=False,
            echo_color=typer.colors.RED,
        )


@app_typer_data_managers.command(
    name=manager_keys.EXTRACT_NPS_FROM_DATABASE_NAME.value,
    help=manager_keys.EXTRACT_NPS_FROM_DATABASE_HELP.value,
    no_args_is_help=True,
)
def extract_nps_from_database(
    data_type: str = typer.Option(
        manager_keys.EXTRACT_NPS_FROM_DATABASE_DATA_DEFAULT.value,
        general_keys.FILE_NAME_LONG.value,
        general_keys.FILE_NAME_SHORT.value,
        help=manager_keys.EXTRACT_NPS_FROM_DATABASE_DATA_HELP.value,
    ),
    text_id: str = typer.Option(
        manager_keys.EXTRACT_NPS_FROM_DATABASE_TEXT_DEFAULT.value,
        manager_keys.EXTRACT_NPS_FROM_DATABASE_TEXT_LONG.value,
        manager_keys.EXTRACT_NPS_FROM_DATABASE_TEXT_SHORT.value,
        help=manager_keys.EXTRACT_NPS_FROM_DATABASE_TEXT_HELP.value,
    ),
) -> None:
    """
    Extrahiert Nominalphrasen (NPs) aus der Datenbank.

    Diese Funktion extrahiert Nominalphrasen (NPs) aus der Datenbank basierend
    auf den angegebenen Parametern.

    Args:
        data_type (str): Der Datentyp, aus dem NPs extrahiert werden sollen.
        text_id (str): Die Text-ID, aus der NPs extrahiert werden sollen.

    Returns:
        None
    """
    corpus = Merlin()
    corpus.sql_command = (
        f"SELECT {data_type} FROM learner_text_data where "
        f"general_author_id = '{text_id}' "
    )
    database_results = corpus.read_merlin_corpus_database()

    if database_results:

        if data_type == "conll":
            incoming = f"user/incoming/conll/{text_id}.conll"
            outgoing = f"user/incoming/pylist/{text_id}.pylist"

            incoming_file = open(incoming, mode="w", encoding="utf-8")

            for row in database_results:
                incoming_file.write(*row)

            incoming_file.close()

            time.sleep(1)

            main_conll_to_pylist(infile=incoming, outfile=outgoing)
            os.remove(incoming)

        # np daten anzeigen
        if data_type == "ast_nps":
            ast_np = AstNominalPhraseExtractor(
                incoming_data=database_results,
                save_name=f"{Gp.RES_AST_NP_FILE.value}_{text_id}.csv",
            )
            ast_results = ast_np.get_ast_data_overview()

            table = Table("Nominale Phrase", "Morphologische Information")
            for entry in ast_results:
                data = ast_results.get(entry)
                status, nominal_phrase = data[:2]
                table.add_row(str(status), str(nominal_phrase))

            console.print(table)
            ast_np.save_extracted_ast_nps()

            typer.secho(
                message=manager_keys.EXTRACT_SAVE_NPS.value,
                fg=typer.colors.GREEN,
            )

    elif not database_results:
        catch_and_log_info(
            custom_message=merlin_keys.INVALID_TEXT_ID.value, echo_msg=True
        )


@app_typer_data_managers.command(
    name=manager_keys.EXTRACT_NPS_LOCAL_NAME.value,
    help=manager_keys.EXTRACT_NPS_LOCAL_HELP.value,
)
def extract_nps_from_local_file(
    ast_file_id: str = typer.Option(
        Gp.TEST_NP_AST_FILE.value,
        general_keys.FILE_NAME_LONG.value,
        general_keys.FILE_NAME_SHORT.value,
        help=general_keys.FILE_NAME_HELP.value,
    ),
    file_type: str = typer.Option(
        manager_keys.EXTRACT_NPS_LOCAL_FILE_DEFAULT.value,
        general_keys.FILE_TYPE_LONG.value,
        general_keys.FILE_NAME_SHORT.value,
        help=manager_keys.EXTRACT_NPS_LOCAL_HELP.value,
    ),
    echo_msg: bool = typer.Option(
        manager_keys.EXTRACT_NPS_LOCAL_ECHO_DEFAULT.value,
        manager_keys.EXTRACT_NPS_LOCAL_ECHO.value,
        manager_keys.EXTRACT_NPS_LOCAL_MUTE.value,
        help=manager_keys.EXTRACT_NPS_LOCAL_ECHO_HELP.value,
    ),
):
    """
    Extrahiert Nominalphrasen (NPs) aus einer lokalen Datei.

    Diese Funktion extrahiert Nominalphrasen (NPs) aus einer lokalen Datei basierend
    auf den angegebenen Parametern.

    Args:
        ast_file_id (str): Der Pfad zur AST-Datei, aus der NPs extrahiert werden sollen.
        file_type (str): Der Dateityp der AST-Datei.
        echo_msg (bool): Wenn True, gibt die Funktion Fortschrittsnachrichten aus.

    Returns:
        None
    """
    try:
        file_id = os.path.basename(ast_file_id)
        if file_type == "ast_nps":
            np_file_handler = AstNominalPhraseExtractor(
                ast_file_name=ast_file_id,
                save_name=f"user/outgoing/extracted_nominal_phrases/{file_id}",
            )
            np_file_handler.save_extracted_ast_nps()

            catch_and_log_info(
                f"Die Ast-Datei {ast_file_id} wurde ausgelesen und die NPs gespeichert ",
                echo_msg=echo_msg,
            )

        if file_type == "pylist":
            np_file_handler = AstNominalPhraseExtractor(
                pylist_name=ast_file_id,
                save_name=f"user/outgoing/extracted_nominal_phrases/nps_{ast_file_id}.csv",
            )
            np_file_handler.save_extracted_ast_nps()

            catch_and_log_info(
                custom_message=manager_keys.EXTRACT_NPS_LOCAL_ECHO_SAVE.value,
                echo_msg=echo_msg,
            )

        if file_type == "conll":
            incoming = f"user/incoming/conll/{ast_file_id}.conll"
            outgoing = f"user/incoming/pylist/{ast_file_id}.pylist"

            main_conll_to_pylist(infile=incoming, outfile=outgoing)

    except Exception as e:
        catch_and_log_error(error=e, custom_message=general_keys.GENERAL_ERROR.value)


@app_typer_data_managers.command(
    name=manager_keys.EXTRACT_DATA_FROM_MERLIN_NAME.value,
    help=manager_keys.EXTRACT_DATA_FROM_MERLIN_HELP.value,
)
def extract_data_from_merlin_database(
    sql_script: str = typer.Option(
        Gp.SQL_MERLIN.value,
        manager_keys.EXTRACT_DATA_FROM_MERLIN_SQL_LONG.value,
        manager_keys.EXTRACT_DATA_FROM_MERLIN_SQL_SHORT.value,
        help=manager_keys.EXTRACT_DATA_FROM_MERLIN_SQL_HELP.value,
    ),
    save_directory=typer.Option(
        Gp.AST_DIR.value,
        general_keys.SAVE_DIR_LONG.value,
        general_keys.SAVE_DIR_SHORT.value,
        help=general_keys.SAVE_DIR_HELP.value,
    ),
    file_extension=typer.Option(
        manager_keys.EXTRACT_DATA_FROM_MERLIN_EXT_DEFAULT.value,
        manager_keys.EXTRACT_DATA_FROM_MERLIN_EXT_LONG.value,
        manager_keys.EXTRACT_DATA_FROM_MERLIN_EXT_SHORT.value,
        help=manager_keys.EXTRACT_DATA_FROM_MERLIN_EXT_HELP.value,
    ),
):
    """
    Extrahiert Daten aus der Merlin-Datenbank.

    Diese Funktion extrahiert Daten aus der Merlin-Datenbank basierend auf den angegebenen Parametern.

    Args:
        sql_script (str): Das SQL-Skript, um Daten abzurufen.
        save_directory (str): Das Verzeichnis, in dem die extrahierten Daten gespeichert werden sollen.
        file_extension (str): Die Dateierweiterung für die gespeicherten Dateien.

    Returns:
        None
    """
    with open(sql_script, "r") as sql_file:
        script = sql_file.read()
    merlin_corpus = Merlin(sql_command=script)
    data = merlin_corpus.read_merlin_corpus_database()
    for text_id in tqdm(data, desc=manager_keys.EXTRACT_AST_DATA_DSC.value):
        merlin_corpus.text_id = text_id[0]
        result = merlin_corpus.extract_merlin_corpus_entry_by_id()
        extracted_element = result.get("ast_nps")

        with open(
            f"{save_directory}/{merlin_corpus.text_id}.{file_extension}",
            mode="w",
            encoding="utf-8-sig",
        ) as r:
            r.write(extracted_element)


@app_typer_data_managers.command(name="np_zu_json", help="Funktion fehlt noch")
def add_np_results_to_np_json_file():
    pass


if __name__ == "__main__":
    app_typer_data_managers()
