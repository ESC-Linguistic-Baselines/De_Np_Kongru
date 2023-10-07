# Standard
import os

# Pip
# None

# Custom

# api_general
# funcs
from kongru.api_general.universal.funcs.basic_logger import catch_and_log_info

from kongru.api_general.statistics.statistics import Statistics


def count_np_results(np_res_files) -> dict:
    """
    Die Ergebnisse aus der NP-Datei werden zusammengetragen und entsprechend gezaehlt.

    Returns:
        statistics_results (dict): Die Ergebnisse der Auszaehlung
    """
    catch_and_log_info("Zaehle die Ergebnisse aus der NP-Datei...", echo_msg=True)
    statistics_results = dict()

    for np_res in np_res_files:
        np_statistics = Statistics(np_results_file=np_res)

        # Text-Id aufstellen
        file_name = os.path.basename(np_res)
        txt_id = file_name.replace(".csv", "").replace("nps_", "")

        # Die Ergebnisse der Zaehlung
        np_results = np_statistics.get_data_as_string()
        statistics_results[txt_id] = np_results

    catch_and_log_info("Ergebnisse erfolgreich gezaehlt!", echo_msg=True)

    return statistics_results


if __name__ == "__main__":
    pass
