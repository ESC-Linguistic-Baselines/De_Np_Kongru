# Standard
import csv
import json

# Pip
# None

# Custom
from kongru.api_general.universal.funcs.get_path_extension import generate_abs_rel_path
from kongru.api_general.universal.constants.general_paths import GeneralPaths as Gp


class NominalPhraseJsonManager:
    def __init__(self, np_json_file, np_csv_file=None):
        self.np_file_json = np_json_file
        self.np_csv_file = np_csv_file

    def read_in_json_file(self):
        with open(self.np_file_json, mode="r") as json_file:
            data = json.load(json_file)
            return data

    def read_in_csv_file(self):
        csv_data = dict()
        with open(self.np_csv_file, mode="r", encoding="utf-8") as csv_file:
            csv_reader = csv.reader(csv_file)
            for row in csv_reader:

                np_id = row[0]
                congruency_code = row[1]
                np = row[2]
                csv_data[np_id] = {
                    "congruency_code": congruency_code,
                    "nominal_phrase": np,
                }

        return csv_data

    def add_np_congruency_information_from_csv_to_json(self):

        json_data = self.read_in_json_file()
        csv_data = self.read_in_csv_file()

        # Ergebnisse
        new_json_data = list()

        for row in json_data:

            sentence_id = row.get("sent_NP_ID")
            np_congruency_info = csv_data.get(sentence_id)
            n = {
                "file_ID": row.get("file_ID"),
                "sent_NP_ID": row.get("sent_NP_ID"),
                "sentence": row.get("sentence"),
                "np_congruency_info": np_congruency_info,
                "metadata": row.get("metadata"),
                "NP_info": row.get("NP_info"),
                "HEAD_info": row.get("HEAD_info"),
                "POST_info": row.get("POST_info"),
                "TOK_info": row.get("TOK_info"),
                "relations": row.get("relations"),
            }
            new_json_data.append(n)

        return new_json_data

    def save_new_json_file(self):

        new_json_data = self.add_np_congruency_information_from_csv_to_json()

        # Neue Dateiname
        files = (self.np_file_json,)
        abs_rel = generate_abs_rel_path(files)
        file_name = list(abs_rel)[0]

        save_dir = f"{Gp.JSON_RES_DIR.value}/{file_name}"

        with open(save_dir, mode="w+") as out_file:
            json.dump(new_json_data, out_file, indent=4)


if __name__ == "__main__":
    pass
