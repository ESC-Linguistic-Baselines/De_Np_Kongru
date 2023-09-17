# Standard
import os
import time

# Pip
from tqdm import tqdm
import typer

from rich.console import Console
from rich.table import Table

# Custom
# api_general

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
    sql_command = (
        "SELECT general_author_id,general_mother_tongue,general_cefr,"
        "txt_len_in_char FROM learner_text_data "
    )
    text_ids = Merlin(sql_command=sql_command).read_merlin_corpus_database()
    table = Table(
        "general_author_id", "general_mother_tongue", "general_cefr", "txt_len_in_char"
    )
    for id_entry in sorted(text_ids):
        table.add_row(*id_entry)
    console.print(table)


@app_typer_data_managers.command(
    name="text_lesen", help="einen bestimmten Text in der Datenbank lesen"
)
def get_and_show_text_by_id(
    text_id: str = typer.Option(
        "1031_0003130",
        "--text_id",
        "--id",
        help="Die Text-Id des gewuenschten Textes angeben",
    )
) -> None:
    entries_extracted_by_text_id = Merlin(
        merlin_txt_id=text_id
    ).extract_merlin_corpus_entry_by_id()
    custom_message = "Die Text-ID, die eingegeben wurde, ist nicht gültig."

    # Nur wenn ein Eintrag vorhanden ist
    if entries_extracted_by_text_id:

        # Die CONLL-Info ist zu viel, daher wird sie entfernt.
        entries_extracted_by_text_id.pop("conll")
        try:
            for entry in entries_extracted_by_text_id:
                typer.echo(f"{entry} {entries_extracted_by_text_id.get(entry)}")
        except Exception as e:
            catch_and_log_error(error=e, custom_message=custom_message)
    else:
        catch_and_log_info(
            msg=custom_message,
            echo_msg=True,
            log_info_message=False,
            echo_color=typer.colors.RED,
        )


@app_typer_data_managers.command(
    name="nps_datenbank",
    help="Nps aus einem bestimmen Datenbankeintrag extrahieren",
    no_args_is_help=True,
)
def extract_nps_from_database(
    data_type: str = typer.Option(
        "ast_nps", "--datei_typ", "--typ" "'ast_nps' oder 'conll' als argument angeben"
    ),
    text_id: str = typer.Option(
        "1023_0001416",
        "--text_id",
        "--id",
        help="Die Text-Id des gewuenschten Textes angeben",
    ),
) -> None:
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

            table = Table("Nominale Phrase", "Morphologische Information ")
            for entry in ast_results:
                data = ast_results.get(entry)
                status, nominal_phrase = data[:2]
                table.add_row(str(status), str(nominal_phrase))

            console.print(table)
            ast_np.save_extracted_ast_nps()

            typer.secho(
                message="Ast-Datei wurde ausgelesen und gespeichert.",
                fg=typer.colors.GREEN,
            )

    elif not database_results:
        catch_and_log_info(msg="Die Eingabe war falsch.", echo_msg=True)


@app_typer_data_managers.command(
    name="nps_datei",
    help="Nps aus einer bestimmen Datei extrahieren",
)
def extract_nps_from_local_file(
    ast_file_id: str = typer.Option(
        2,
        "--datei_name",
        "--name",
        help="Der Name der Datei, die ausgewertet werden soll.",
    ),
    file_type: str = typer.Option(
        "ast_nps", "--datei_typ", "--typ", help="Dateitypen ast_nps, pylist, conll"
    ),
    echo_msg: bool = typer.Option(
        "echo", "--echo", "--e", help="Die Fortschittsdaten in der Konsole anzeigen"
    ),
):
    try:
        file_id = os.path.basename(ast_file_id)
        if file_type == "ast_nps":

            np_file_handler = AstNominalPhraseExtractor(
                ast_file_id=ast_file_id,
                save_name=f"user/outgoing/extracted_nominal_phrases/{file_id}",
            )
            np_file_handler.save_extracted_ast_nps()

            catch_and_log_info(
                f"Die Ast-Datei {ast_file_id} wurde ausgelesen und die NPs ",
                echo_msg=echo_msg,
            )

        if file_type == "pylist":
            np_file_handler = AstNominalPhraseExtractor(
                pylist_name=ast_file_id,
                save_name=f"user/outgoing/extracted_nominal_phrases/nps_{ast_file_id}.csv",
            )
            np_file_handler.save_extracted_ast_nps()

            typer.secho(
                message="Ast-Datei wurde ausgelesen und gespeichert.",
                fg=typer.colors.GREEN,
            )

        if file_type == "conll":
            incoming = f"user/incoming/conll/{ast_file_id}.conll"
            outgoing = f"user/incoming/pylist/{ast_file_id}.pylist"

            main_conll_to_pylist(infile=incoming, outfile=outgoing)

    except Exception as e:
        catch_and_log_error(error=e, custom_message="Ein Fehler ist aufgetreten.")


@app_typer_data_managers.command(
    name="daten_extrahieren", help="Die Befehle ausfuehren aus der SQL-Datei"
)
def extract_data_from_merlin_database(
    sql_script: str = typer.Option(
        Gp.SQL_MERLIN.value, "--sql_script", "--sql", help="Name der SQL datei"
    ),
    save_directory=typer.Option(
        Gp.AST_DIR.value,
        "--speichern-verzeichnis",
        "--speichern",
        help="Verzeichnis, worin die Ergebnisse gespeichert werden",
    ),
    file_extension=typer.Option(
        "ast", "--datei_endung", "--endung", help="Die Endung der Datei"
    ),
):

    with open(sql_script, "r") as sql_file:
        script = sql_file.read()
    merlin_corpus = Merlin(sql_command=script)
    data = merlin_corpus.read_merlin_corpus_database()
    for text_id in tqdm(data, desc="Ast-Dateien extrahieren"):
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
    pass
