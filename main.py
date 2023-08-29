# Standard
import glob
import os

# Pip
import typer

# Custom

# api_general
from kongru.api_general.database_managers.app_data_managers import (
    app_typer_data_managers,
)

# constants
from kongru.api_general.universal.constants.message_keys import MessageKeys as Mk
from kongru.api_general.universal.constants.general_paths import GeneralPaths as Gp

# funcs
from kongru.api_general.universal.funcs.basic_logger import (
    catch_and_log_error,
    catch_and_log_info,
)

# api_nlp
# analyse
from kongru.api_nlp.congruential_analysis.app_congruential_analysis import (
    app_typer_congruential_analysis,
)

# Haupt-Typer App
main_typer_app = typer.Typer(
    add_help_option=False,
    no_args_is_help=True,
    name="DE Np Kongru",
    add_completion=False,
)

# Die Sub-Typer apps, die hier zusammengefasst werden.
main_typer_app.add_typer(app_typer_congruential_analysis)
main_typer_app.add_typer(app_typer_data_managers)


@main_typer_app.command(
    help="Ein ausgewaehltes Verzeichnis leeren", name="verzeichnis_leeren"
)
def empty_chosen_directory(
    trg_dir: str = typer.Option(
        Gp.DIR_LOG.DIR_LOG.value,
        "--trg_dir",
        "--trg",
        help="Das Verzeichnis, das geleert werden soll.",
    ),
    file_type: str = typer.Option(
        "log",
        "--datei_type",
        "--datei",
        help="Die Dateien, die geloescht werden sollen.",
    ),
) -> None:
    files_to_be_deleted = f"{trg_dir}/*.{file_type}"
    file_directory = glob.glob(files_to_be_deleted)

    if file_directory:
        for file in file_directory:
            os.remove(file)

        catch_and_log_info(
            msg=f"die Dateien {files_to_be_deleted} wurden geloescht.", echo_msg=True
        )
    else:
        catch_and_log_info(
            msg=f"die Dateien {files_to_be_deleted} existieren nicht.", echo_msg=True
        )


if __name__ == "__main__":
    try:
        main_typer_app()
        catch_and_log_info(msg="Anwendung wurde gestartet.")
    except Exception as e:
        msg = Mk.Main.ERR_MAIN_APP.value
        catch_and_log_error(error=e, custom_message=msg, kill_if_fatal_error=True)
