# Standard
import csv

from collections import OrderedDict

# Pip
# None

# Custom
from kongru.api_general.universal.constants.general_paths import GeneralPaths as Gp


class Statistics:
    def __init__(self, np_results_file=None):
        self.np_results_file = np_results_file
        self.header_file = Gp.NP_HEADER_FILE.value

    def __open_file(self):
        with open(self.np_results_file, mode="r", encoding="utf-8") as file:
            csv_reader = csv.reader(file)
            return list(csv_reader)

    def get_file_header(self):
        header_file = open(self.header_file, mode="r", encoding="utf-8")
        csv_header = [i for i in header_file]
        header_results, merlin_meta_data = OrderedDict(), list()

        for row in csv_header:
            if row.strip().isupper():
                header_results[row.strip()] = 0
            else:
                merlin_meta_data.append(row)

        data = {"header_results": header_results, "merlin_meta_data": merlin_meta_data}

        header_file.close()
        return data

    def create_csv_results_file(self):
        csv_header = list(self.get_file_header().get("header_results").keys())

        meta_data = self.get_file_header().get("merlin_meta_data")
        meta_data = [i.strip() for i in meta_data]

        # Ergebniss-Datei aufstellen
        save_data = Gp.NP_MAIN_SAVE_FILE.value
        csv_writer = csv.writer(open(save_data, mode="w+"))

        csv_writer.writerow(meta_data + csv_header)

        return csv_writer

    def count_congruency_codes(self):
        np_result_data = self.__open_file()
        data_set = OrderedDict(
            [
                ("EINFACH", {"0": 0, "10": 0}),
                ("ART", {"1": 0, "11": 0}),
                ("PREP", {"2": 0, "12": 0}),
                ("EIGENNAMEN", {"3": 0}),
                ("REDEWENDUNGEN", {"4": 0}),
                ("GESAMT_WAHR", 0),
                ("GESAMT_FALSCH", 0),
                ("GESAMT_UNBEKANNT", 0),
            ]
        )

        for row in np_result_data:
            code = int(row[0])

            if code == 0:
                data_set["EINFACH"]["0"] += 1
                data_set["GESAMT_WAHR"] += 1
            elif code == 1:
                data_set["ART"]["1"] += 1
                data_set["GESAMT_WAHR"] += 1
            elif code == 2:
                data_set["PREP"]["2"] += 1
                data_set["GESAMT_WAHR"] += 1
            elif code == 3:
                data_set["EIGENNAMEN"]["3"] += 1
                data_set["GESAMT_WAHR"] += 1
            elif code == 4:
                data_set["REDEWENDUNGEN"]["4"] += 1
                data_set["GESAMT_WAHR"] += 1
            elif code == 10:
                data_set["EINFACH"]["10"] += 1
                data_set["GESAMT_FALSCH"] += 1
            elif code == 11:
                data_set["ART"]["11"] += 1
                data_set["GESAMT_FALSCH"] += 1
            elif code == 12:
                data_set["PREP"]["12"] += 1
                data_set["GESAMT_FALSCH"] += 1
            else:
                data_set["GESAMT_UNBEKANNT"] += 1

        return data_set

    def get_data_as_string(self):

        code_data = self.get_file_header().get("header_results")
        codes = self.count_congruency_codes()

        for row in codes:
            if row == "ART":

                congru, not_congru = codes.get(row).values()
                code_data["ART"] = congru
                code_data["ART_NICHT"] = not_congru

            elif row == "EINFACH":
                congru, not_congru = codes.get(row).values()
                code_data["EINFACH"] = congru
                code_data["EINFACH_NICHT"] = not_congru

            elif row == "PREP":
                congru, not_congru = codes.get(row).values()
                code_data["PREP"] = congru
                code_data["PREP_NICHT"] = not_congru
            elif row == "PREP":
                congru, not_congru = codes.get(row).values()
                code_data["PREP"] = congru
                code_data["PREP_NICHT"] = not_congru

            elif row == "EIGENNAMEN":
                congru = codes.get(row).get("3")
                code_data["EIGENNAMEN"] = congru

            elif row == "REDEWENDUNGEN":
                congru = codes.get(row).get("4")
                code_data["REDEWENDUNGEN"] = congru

            elif row == "GESAMT_UNBEKANNT":
                congru = codes.get(row)
                code_data["GESAMT_UNBEKANNT"] = congru

            elif row == "GESAMT_WAHR":
                congru = codes.get(row)
                code_data["GESAMT_WAHR"] = congru

            elif row == "GESAMT_FALSCH":
                congru = codes.get(row)
                code_data["GESAMT_FALSCH"] = congru

        return code_data


if __name__ == "__main__":
    res = Statistics().get_file_header()
