# Standard
import csv

# Pip
# None

# Custom
# None


class Statistics:
    def __init__(self, np_results_file=None):
        self.np_results_file = np_results_file

    def __open_file(self):
        with open(self.np_results_file, mode="r", encoding="utf-8") as file:
            csv_reader = csv.reader(file)
            return list(csv_reader)

    def count_congruency_codes(self):

        np_result_data = self.__open_file()
        data_set = {
            "ART": {0: 0, "11": 0},
            "PREP": {"5": 0, "15": 0},
            "RECHTSCHREIBUNG": {"5": 0, "15": 0},
            "EIGENNAMEN": {"5": 0, "15": 0},
            "REDEWENDUNGEN": {"5": 0, "15": 0},
            "UNBEKANNT": 0,
        }

        for row in np_result_data:
            code = int(row[0])
            # ART NPS
            if code == 5:
                data_set["PREP"]["5"] = data_set["PREP"]["5"] + 1
            if code == 15:
                data_set["PREP"]["15"] = data_set["PREP"]["15"] + 1

        return data_set

    def get_data_as_string(self):
        code_data = {
            "EINFACH": 0,
            "EINFACH_NICHT": 0,
            "ART": 0,
            "ART_NICHT": 0,
            "PREP": 0,
            "PREP_NICHT": 0,
            "RECHTSCHREIBUNG": 0,
            "RECHTSCHREIBUNG_NICHT": 0,
            "EIGENNAMEN": 0,
            "EIGENNAMEN_NICHT": 0,
            "REDEWENDUNGEN": 0,
            "REDEWENDUNGEN_NICHT": 0,
        }

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
            elif row == "RECHTSCHREIBUNG":
                congru, not_congru = codes.get(row).values()
                code_data["RECHTSCHREIBUNG"] = congru
                code_data["RECHTSCHREIBUNG_NICHT"] = not_congru
            elif row == "EIGENNAMEN":
                congru, not_congru = codes.get(row).values()
                code_data["EIGENNAMEN"] = congru
                code_data["EIGENNAMEN_NICHT"] = not_congru
            elif row == "REDEWENDUNGEN":
                congru, not_congru = codes.get(row).values()
                code_data["REDEWENDUNGEN"] = congru
                code_data["REDEWENDUNGEN_NICHT"] = not_congru

        return code_data


if __name__ == "__main__":
    pass
