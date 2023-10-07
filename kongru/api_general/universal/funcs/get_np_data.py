# Standard
# None
import glob

from tqdm import tqdm

# Pip
# None

# Custom

# api_general
from kongru.api_general.database_managers.app_data_managers import (
    extract_nps_from_local_file,
)
from kongru.api_general.universal.funcs.basic_logger import catch_and_log_info


def np_data() -> None:
    """
    Die Nominalphrasen aus den jeweiligen Ast-Dateien extrahieren

    Returns:
        None
    """
    catch_and_log_info("Extrahiere Nominalphrasen aus AST-Dateien...", echo_msg=False)

    # Nominalphrasen aus dem Ast verzeichnis extrahieren
    ast_id_number = glob.glob("user/incoming/ast/*.*")
    for id_num in tqdm(ast_id_number, desc="NPs extrahieren", unit=" Ast-Datei"):
        extract_nps_from_local_file(
            ast_file_id=id_num, file_type="ast_nps", echo_msg=False
        )

    catch_and_log_info("Nominalphrasen erfolgreich extrahiert!", echo_msg=False)


if __name__ == "__main__":
    pass
