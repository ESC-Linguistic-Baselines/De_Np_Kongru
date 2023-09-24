# Standard
import glob
import os

# Pip
from tqdm import tqdm

# Custom

from kongru.api_general.database_managers.managers.merlin_manager import MerlinManager
from kongru.api_general.database_managers.app_data_managers import (
    extract_data_from_merlin_database,
    extract_nps_from_local_file,
)
from kongru.api_general.universal.constants.general_paths import GeneralPaths as Gp
from kongru.api_general.universal.constants import general_vars as gv
from kongru.api_general.statistics.statistics import Statistics
from kongru.api_general.universal.funcs.basic_logger import (
    catch_and_log_info,
    catch_and_log_error,
)
from kongru.api_general.universal.constants.message_keys import MessageKeys as Mk

congruential_keys = Mk.AppCongruentialAnalysis


def get_ast_data() -> None:
    """
     AST Dateien aus der Datenbank-extrahieren
    Returns:
        None
    """
    extract_data_from_merlin_database(
        sql_script=Gp.SQL_MERLIN.value,
        save_directory=Gp.AST_DIR.value,
        file_extension="ast",
    )

    catch_and_log_info(congruential_keys.AST_DATA_EXTRACTED.value, echo_msg=False)


def get_np_data() -> None:
    """
    Die Nominalphrasen aus den jeweiligen Ast-Dateien extrahieren
    Returns:
        None
    """
    catch_and_log_info(congruential_keys.NP_DATA_EXTRACT.value, echo_msg=False)

    # Nominalphrasen aus dem Ast verzeichnis extrahieren
    ast_id_number = glob.glob("user/incoming/ast/*.*")
    for id_num in tqdm(ast_id_number, desc="NPs extrahieren", unit=" Ast-Datei"):
        extract_nps_from_local_file(
            ast_file_id=id_num, file_type="ast_nps", echo_msg=False
        )

    catch_and_log_info(congruential_keys.NP_DATA_EXTRACTED.value, echo_msg=False)


def count_np_results(np_res_files) -> dict:
    """
    Die Ergebnisse aus der NP-Datei werden zusammengetragen und
    entsprechend gezaehlt.

    Returns:
        statistics_results (dict): Die Ergebnisse der Auszaehlung
    """
    catch_and_log_info(congruential_keys.NP_COUNT_RESULTS.value, echo_msg=True)
    statistics_results = dict()

    for np_res in np_res_files:
        np_statistics = Statistics(np_results_file=np_res)

        # Text-Id aufstellen
        file_name = os.path.basename(np_res)
        txt_id = file_name.replace(".csv", "").replace("nps_", "")

        # Die Ergebnisse der Zaehlung
        np_results = np_statistics.get_data_as_string()
        statistics_results[txt_id] = np_results

    catch_and_log_info(congruential_keys.NP_RESULTS_COUNTED.value, echo_msg=True)

    return statistics_results


def generate_results_file(collective_results) -> None:
    """
    Die Ergebnisse werden hier zusammengetragen und in der entsprechenden
    CSV-Ergebnisse-Datei gespeichert.

    Args:
        collective_results (dict): Die Ergebnisse der Auszaehlung

    Returns:
        None
    """
    catch_and_log_info(congruential_keys.GENERATE_RESULT_FILES.value, echo_msg=True)

    # Header-Datei aufstellen
    statistics = Statistics()
    csv_data = statistics.create_csv_results_file()

    for txt_id in collective_results:
        command = gv.SQL_MERLIN_META_DATA_QUERY.replace("(?)", f"'{txt_id}'")
        meta_data_text = MerlinManager(sql_command=command)

        try:
            corpus_data = meta_data_text.read_merlin_corpus_database()
            merlin_sql_result = list(corpus_data[0])
            txt_id_data = list(collective_results.get(txt_id).values())
            new_data = merlin_sql_result + txt_id_data
            # Ergebnisse speichern
            csv_data.writerow(new_data)
        except Exception as e:
            catch_and_log_error(
                error=e,
                custom_message=congruential_keys.RESULT_FILES_CREATED.value,
                echo_msg=False,
            )

    catch_and_log_info(congruential_keys.RESULT_FILES_CREATED.value, echo_msg=True)


if __name__ == "__main__":
    pass
