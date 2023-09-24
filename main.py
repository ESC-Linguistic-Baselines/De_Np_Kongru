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
from kongru.api_general.statistics.app_statistics import (
    app_typer_statics,
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

# Message Keys als Enum
main_keys = Mk.MainApp
general_keys = Mk.General

# Haupt-Typer App
main_typer_app = typer.Typer(
    add_help_option=False,
    no_args_is_help=True,
    name=main_keys.APP_NAME.value,
    help=main_keys.APP_NAME_HELP.value,
    add_completion=False,
)

# Die Sub-Typer apps, die hier zusammengefasst werden.
main_typer_app.add_typer(app_typer_congruential_analysis)
main_typer_app.add_typer(app_typer_data_managers)
main_typer_app.add_typer(app_typer_statics)


@main_typer_app.command(
    help=main_keys.EMPTY_DIRECTORY.value, name=main_keys.EMPTY_DIRECTORY_HELP.value
)
def empty_chosen_directory(
    trg_dir: str = typer.Option(
        Gp.LOG_DIR.LOG_DIR.value,
        main_keys.EMPTY_DIRECTORY_TRG_LONG.value,
        main_keys.EMPTY_DIRECTORY_TRG_SHORT.value,
        help=main_keys.EMPTY_DIRECTORY_TRG_HELP.value,
    ),
    file_type: str = typer.Option(
        general_keys.FILE_TYPE_LOG.value,
        general_keys.FILE_TYPE_LONG.value,
        general_keys.FILE_TYPE_SHORT.value,
        help=main_keys.FILE_TYPE_HELP.value,
    ),
) -> None:

    if file_type == "alle":
        file_type = "*"

    file_directory = f"{trg_dir}/*.{file_type}"
    files_to_be_deleted = glob.glob(file_directory)

    folder_path = os.path.exists(trg_dir)
    is_file_directory_emtpy = bool(file_directory)

    if len(files_to_be_deleted) > 0 and folder_path is True:
        for file in files_to_be_deleted:
            os.remove(file)

        catch_and_log_info(
            custom_message=f"Die Dateien '{file_directory}' wurden geloescht.",
            echo_msg=True,
        )

    elif len(files_to_be_deleted) == 0 and folder_path is True:
        catch_and_log_info(
            custom_message=f"Der Ordner '{trg_dir}' ist schon leer.", echo_msg=True
        )

    else:
        catch_and_log_info(
            custom_message=f"Ein unbekannter Fehler ist aufgetreten", echo_msg=True
        )


if __name__ == "__main__":
    try:
        main_typer_app()
        catch_and_log_info(custom_message=main_keys.MAIN_APP_START.value)
    except Exception as e:
        msg = Mk.MainApp.MAIN_APP_FATAL_ERROR.value
        catch_and_log_error(error=e, custom_message=msg, kill_if_fatal_error=True)
