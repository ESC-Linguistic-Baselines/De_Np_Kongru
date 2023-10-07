# Standard
import glob

# Pip
from tqdm import tqdm

# Custom
# api_general

# funcs
from kongru.api_general.universal.funcs.get_path_extension import generate_abs_rel_path

# const
from kongru.api_general.universal.constants.general_paths import GeneralPaths as Gp

# managers
from kongru.api_general.database_managers.managers.merlin_manager import MerlinManager

from kongru.api_general.database_managers.managers.nominal_phrase_json_manager import (
    NominalPhraseJsonManager as Npjm,
)


def generate_np_json_files(text_id_source) -> None:
    """
    die zugehoerige Json-Daten werden fuer jede Np-Id aus der Merlin-Corpus-Datenbank
    extrahiert. Diese werden dann anschließend gespeichert.

    Args:
        text_id_source (list): Ids, die aus der Datenbank extrahiert werden sollen.

    Returns:
        None
    """
    for text_id in tqdm(text_id_source, desc="Processing Text IDs"):
        merlin = MerlinManager()
        merlin.sql_command = f"""
        select json_nps from learner_text_data where general_author_id = '{text_id}'
        """

        res = merlin.read_merlin_corpus_database()

        file_name = f"{Gp.JSON_INCOMING_DIR.value}/{text_id}.json"
        with open(file_name, encoding="utf-8", mode="w") as outfile:
            data = res[0][0]
            outfile.write(data)


def combine_csv_json_data() -> None:
    """
    Die Dateien aus der .csv-Datei und .json Datei werden zusammen gefuehrt.

    Hinweis:
        Die Dateien werden nur zusammengefuehrt, wenn es sowohl eine .csv-Datei
        als auch eine .json Datei.

    Returns:
        None
    """
    csv_data = glob.glob(Gp.NP_CSV_RES_FILES_GLOB.value)
    json_data = glob.glob(Gp.NP_JSON_RAW_FILES_GLOB.value)

    csv_files = generate_abs_rel_path(csv_data)
    json_files = generate_abs_rel_path(json_data)

    stripped_json_keys = [f.replace(".json", "") for f in json_files]

    for cfile in tqdm(csv_files, desc="Converting CSV to JSON"):
        stripped_csv_file = cfile.replace(".csv", "")
        if stripped_csv_file in stripped_json_keys:
            c = cfile
            j = cfile.replace(".csv", ".json")

            csv_json_convert = Npjm(
                np_json_file=json_files.get(j), np_csv_file=csv_files.get(c)
            )
            csv_json_convert.save_new_json_file()


if __name__ == "__main__":
    combine_csv_json_data()
