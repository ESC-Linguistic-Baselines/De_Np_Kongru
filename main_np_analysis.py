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
)
from kongru.api_general.universal.constants.general_paths import GeneralPaths as Gp
from kongru.api_general.statistics.statistics import Statistics
from kongru.api_general.database_managers.app_data_managers import (
    extract_nps_from_local_file,
)

# AST Dateien aus der Datenbank-extrahieren
# extract_data_from_merlin_database( sql_script=Gp.SQL_MERLIN.value, save_directory=Gp.AST_DIR.value, file_extension="ast")

# Nominalphrasen aus dem Ast verzeichnis extrahieren
ast_id_number = glob.glob("user/incoming/ast/*.*")
for id_num in ast_id_number:
    file_name = os.path.basename(id_num).replace(".ast", " ")

    f = extract_nps_from_local_file(ast_file_id=id_num, file_type="ast_nps")


# extract_nps_from_local_file( file_name=ast_file, file_type="ast_nps")
np_extracted_files = glob.glob("user/outgoing/extracted_nominal_phrases/*.*")

# Np Kongruenz bestimmen und die Ergebnisse speichern
for np_ext_file in np_extracted_files:
    file_name = os.path.basename(np_ext_file)

    nominal_phrase_agreement_analysis(file_name=np_ext_file,
                                      save_file=file_name)
    break

# NP Codes zählen
statistics = Statistics()
np_res_files = glob.glob("user/outgoing/nominal_phrase_analysis_results/*.*")

collective_results = dict()

for np_res in np_res_files:
    statistics.np_results_file = np_res
    file_name = os.path.basename(np_res)
    txt_id = file_name.replace(".csv", "").replace("nps_", "")
    np_results = statistics.get_data_as_string()
    collective_results[txt_id] = np_results


# Dateien zuordnen
header_file = open(
    r"/Users/christopherchandler/repo/Python/computerlinguistik/"
    r"de_np_kongru/dokumentation/results/header_file.csv",
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

    merlin_manager = MerlinManager(
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
    merlin_sql_result = list(merlin_manager.read_merli_corpus_database()[0])
    txt_id_dta = list(collective_results.get(txt_id).values())
    new_data = merlin_sql_result + txt_id_dta

    # Ergebnisse speichern

    csv_writer.writerow(new_data)

if __name__ == "__main__":
    pass
