# Standard
import glob
import os

import typer
# Pip
from tqdm import tqdm

# Custom
from kongru.api_nlp.congruential_analysis.app_congruential_analysis import (
    nominal_phrase_agreement_analysis,
)
from kongru.api_general.database_managers.managers.merlin_manager import MerlinManager
from kongru.api_general.database_managers.app_data_managers import (
    extract_data_from_merlin_database,
    extract_nps_from_local_file,
)
from kongru.api_general.universal.constants.general_paths import GeneralPaths as Gp
from kongru.api_general.universal.constants import general_vars as gv
from kongru.api_general.statistics.statistics import Statistics
from kongru.api_general.universal.funcs.basic_logger import catch_and_log_info


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

    catch_and_log_info("AST-Dateien erfolgreich extrahiert!", echo_msg=True)


def get_np_data() -> None:
    """
    Die Nominalphrasen aus den jeweiligen Ast-Dateien extrahieren
    Returns:
        None
    """
    catch_and_log_info("Extrahiere Nominalphrasen aus AST-Dateien...", echo_msg=True)

    # Nominalphrasen aus dem Ast verzeichnis extrahieren
    ast_id_number = glob.glob("user/incoming/ast/*.*")
    for id_num in tqdm(
        ast_id_number, desc="Ast-Dateien verarbeiten", unit=" Ast-Datei"
    ):
        extract_nps_from_local_file(
            ast_file_id=id_num, file_type="ast_nps", echo_msg=False
        )

    catch_and_log_info("Nominalphrasen erfolgreich extrahiert!", echo_msg=True)


def run_congruency(
    np_files: list, id_numbers: list, text_limit: int = 0, all_texts: bool = False
) -> None:
    """
    Hier wird die Hauptanalyse ausgefuehrt.

    Args:
        all_texts(bool): Alle Texte sollen analysiert werden.
        np_files(list): Die Dateien, die analysiert werden sollen.
        id_numbers(list): Die  Text-Id-Nummer der Texte, die anaylsiert werden sollen.
        text_limit (int):  Die Anzahl der Dateien, die analysiert werdne sollen.

    Returns:


    """
    # Np Kongruenz bestimmen und die Ergebnisse speichern
    count = 0
    for np_ext_file in np_files:

        # Text-Id aufstellen

        file_name = os.path.basename(np_ext_file)
        txt_id = file_name.replace(".csv", "")

        if txt_id in id_numbers:
            catch_and_log_info(
                f"Text-Id {txt_id}: " f"Führe Hauptanalyse durch...", echo_msg=True
            )
            nominal_phrase_agreement_analysis(
                file_name=np_ext_file, save_file=file_name
            )
            count += 1

            if all_texts and text_limit == 0:
                text_limit = len(id_numbers)
            elif count > text_limit:
                break

            catch_and_log_info(
                f"Text-Id {txt_id}: " f"Hauptanalyse abgeschlossen \n", echo_msg=True
            )

            progress = count / text_limit
            blocks = round(progress % 1 * 10)
            count_down = 10 - blocks
            remaining_prog = count_down * "#"
            current_prog = "#" * blocks
            prog_res = (
                f"Fortschritt: {current_prog}/{remaining_prog}, "
                f"Aktuell: {count}, Gesamt: {text_limit}"
            )

            if blocks == 0:
                full_bar = "#" * 10
                prog_res = (
                    f"Fortschritt:  {full_bar} Aktuell: {count}, Gesamt: {text_limit}"
                )
                typer.echo(prog_res)
            else:
                typer.echo(prog_res)


def count_np_results() -> dict:
    """
    Die Ergebnisse aus der NP-Datei werden zusammengetragen und
    entsprechend gezaehlt.

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
        print(np_results)
        statistics_results[txt_id] = np_results

    catch_and_log_info("Ergebnisse erfolgreich gezaehlt!", echo_msg=True)

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
    catch_and_log_info("Generiere Ergebnisdatei...", echo_msg=True)

    # Header-Datei aufstellen
    statistics = Statistics()
    csv_data = statistics.create_csv_results_file()

    for txt_id in collective_results:
        command = gv.MERLIN_META_DATA_QUERY.replace("(?)", f"'{txt_id}'")
        meta_data_text = MerlinManager(sql_command=command)

        merlin_sql_result = list(meta_data_text.read_merlin_corpus_database()[0])
        txt_id_data = list(collective_results.get(txt_id).values())
        new_data = merlin_sql_result + txt_id_data

        # Ergebnisse speichern
        csv_data.writerow(new_data)

    catch_and_log_info("Ergebnisdatei erfolgreich generiert!", echo_msg=True)


if __name__ == "__main__":
    # Dateien aufstellen
    ids = open(Gp.NP_TRAINING_IDS.value, mode="r", encoding="utf-8").readlines()
    training_ids = [i.strip() for i in ids]
    np_extracted_files = glob.glob("user/outgoing/extracted_nominal_phrases/*.*")
    np_res_files = glob.glob("user/outgoing/nominal_phrase_analysis_results/*.*")

    # get_ast_data()
    # get_np_data()
    #run_congruency(np_extracted_files, training_ids,all_texts=True)
    count_results = count_np_results()
    generate_results_file(count_results)
