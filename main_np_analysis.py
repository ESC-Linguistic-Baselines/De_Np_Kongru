# Standard
import csv
import glob
import os

# Pip
# None

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
from kongru.api_general.statistics.statistics import Statistics


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


def get_np_data():
    # Nominalphrasen aus dem Ast verzeichnis extrahieren
    ast_id_number = glob.glob("user/incoming/ast/*.*")
    for id_num in ast_id_number:
        extract_nps_from_local_file(ast_file_id=id_num,
                                    file_type="ast_nps")


def run_congruency(np_extracted_files, id_numbers, count=0):
    # Np Kongruenz bestimmen und die Ergebnisse speichern
    for np_ext_file in np_extracted_files:

        file_name = os.path.basename(np_ext_file)
        txt_id = file_name.replace(".csv", "")

        if txt_id in id_numbers:
            nominal_phrase_agreement_analysis(
                file_name=np_ext_file, save_file=file_name
            )
            count += 1
            if count == 5: break


def count_np_results():
    statistics = Statistics()
    collective_results = dict()

    for np_res in np_res_files:
        statistics.np_results_file = np_res
        file_name = os.path.basename(np_res)
        txt_id = file_name.replace(".csv", "").replace("nps_", "")
        np_results = statistics.get_data_as_string()
        collective_results[txt_id] = np_results

    return collective_results


def generate_results_file(collective_results):
    # Ergebnisse speichern
    # Dateien zuordnen
    header_file = open(
        r"/Users/christopherchandler/repo/Python/computerlinguistik/"
        r"de_np_kongru/dokumentation/project_layout/header_file.csv",
        mode="r",
        encoding="utf-8",
    )

    csv_header = list(csv.reader(header_file))[0]

    # Ergebnisse-Datei aufstellen
    save_data = (
        "/Users/christopherchandler/repo/Python/computerlinguistik"
        "/de_np_kongru/dokumentation/results/batch_evaluation_np.csv"
    )

    csv_writer = csv.writer(open(save_data, mode="w+"))
    csv_writer.writerow(csv_header)

    for txt_id in collective_results:
        meta_data_text = MerlinManager(
            sql_command=f"""
            SELECT general_author_id, general_test_language, general_cefr,
            general_task, general_mother_tongue, general_age, general_gender,
            rating_overall_cefr_rating, rating_grammatical_accuracy, rating_orthography,
            rating_vocabulary_range, rating_vocabulary_control, rating_coherence_cohesion,
            rating_sociolinguistic_appropriateness, txt_len_in_char
            FROM learner_text_data
            WHERE general_author_id = '{txt_id}'
            """
        )

        # NP daten zusammentragen und kombinieren
        merlin_sql_result = list(meta_data_text.read_merli_corpus_database()[0])
        txt_id_dta = list(collective_results.get(txt_id).values())
        new_data = merlin_sql_result + txt_id_dta

        csv_writer.writerow(new_data)


if __name__ == "__main__":
    # Dateien
    ids = open(
        "/Users/christopherchandler/repo/Python/computerlinguistik/"
        "de_np_kongru/dokumentation/results/test_ids.txt"
    ).readlines()
    np_extracted_files = glob.glob("user/outgoing/extracted_nominal_phrases/*.*")
    np_res_files = glob.glob("user/outgoing/nominal_phrase_analysis_results/*.*")
    save_data = (
        "/Users/christopherchandler/repo/Python/computerlinguistik"
        "/de_np_kongru/dokumentation/results/batch_evaluation_np.csv"
    )
    csv_writer = csv.writer(open(save_data, mode="w+"))

    training_ids = [i.strip() for i in ids]
    # get_ast_data()
    # get_np_data()
    # run_congruency(np_extracted_files, training_ids)
    collective_results = count_np_results()
    generate_results_file(collective_results)
