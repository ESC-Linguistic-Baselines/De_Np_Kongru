# Standard
# None

# Pip
# None

# Custom

# funcs
from kongru.api_general.universal.funcs.basic_logger import catch_and_log_info

# constants
from kongru.api_general.universal.constants.general_paths import GeneralPaths as Gp

# manager
from kongru.api_general.database_managers.app_data_managers import (
    extract_data_from_merlin_database,
)


def ast_data() -> None:
    """
    AST Dateien aus der Datenbank-extrahieren und fuer Weiterverabeitung speichern.

    Returns:
        None
    """
    extract_data_from_merlin_database(
        sql_script=Gp.SQL_MERLIN.value,
        save_directory=Gp.AST_DIR.value,
        file_extension="ast",
    )

    catch_and_log_info("AST-Dateien erfolgreich extrahiert!", echo_msg=False)


if __name__ == "__main__":
    pass
