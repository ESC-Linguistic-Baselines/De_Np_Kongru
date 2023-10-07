# Standard
import csv
import pickle

# Pip
# None

# Custom

# api_general
# constants
from kongru.api_general.universal.constants.general_paths import GeneralPaths as Gp


class DemorphyManager:
    """
    Ein Manager fuer Demorphy-Daten, der verschiedene Ressourcen und Dateien verwaltet.
    Hier wird die Demoprhy-Dict-Datei und die Lemmata eingelesen
    """

    def __init__(
        self,
        file_name=Gp.TEST_NP_FILE_CSV.value,
    ):
        self.demorphy_dict = Gp.DB_DEMORPHY_TXT.value
        self.lemma_txt = Gp.DB_DEMORPHY_LEMMA_TXT.value
        self.file_name = file_name

    def get_read_in_demorphy_dict(self, read_in_pickle_dict: bool = True):
        """
        Diese Methode liest Demorphy-Daten aus einer Datei oder einem Pickle-Objekt
        und gibt sie zurueck.

        Args:
            read_in_pickle_dict (bool, optional): Wenn True, wird das Pickle-Objekt
            verwendet, andernfalls die Datei.
                Standardmaessig True.

        Returns:
            demorphy_dict_data(dict): Ein Dictionary, das die Demorphy-Daten enthaelt.
        """

        # Wenn 'read_in_pickle_dict' True ist, wird das Pickle-Objekt verwendet
        if read_in_pickle_dict:
            with open(Gp.DB_DEMORTHY_PKL.value, "rb") as pickle_file:
                data = pickle.load(pickle_file)
                return data

        # Andernfalls wird die Demorphy-Datei gelesen
        else:
            demorphy_dict_data = {}

            with open(self.demorphy_dict, mode="r", encoding="utf-8") as out_going:
                data = out_going.readlines()

                # Schleife durch die Daten und erstelle das Dictionary
                for row in data:
                    row_data = row.strip().split(" ")

                    # Wenn eine Zeile nur einen Eintrag enthaelt, wird ein leerer Wert erstellt
                    if len(row_data) == 1:
                        key = row.strip()
                        demorphy_dict_data[key] = []
                    else:
                        demorphy_dict_data[key].append(row.strip())

            return demorphy_dict_data

    def get_read_in_np_file(self) -> dict:
        """
        Diese Methode liest Informationen aus einer CSV-Datei ein und
        strukturiert sie in einem Python-Dictionary.
        Das Dictionary enthaelt eine uebersicht ueber Nominalphrasen (NPs)
        in Form von Schluessel-Wert-Paaren.

        Returns:
            np_data(dict): Ein dict,
            das die eingelesenen Daten enthaelt, strukturiert nach bestimmten Kriterien.
        """
        # Initialisierung von Variablen und Listen zur Kategorisierung von Merkmalen
        file_name = self.file_name  # Der Dateiname der CSV-Datei

        np_data = {}  # Ein Dictionary zur Speicherung der eingelesenen Daten

        # Listen zur Kategorisierung von morphologischen Merkmalen
        case = "Acc", "Dat", "Nom", "Gen"
        gender = "Fem", "Neut", "Masc"
        number = "Pl", "Sg"
        article = "Def", "Indef"

        # oeffnen der CSV-Datei und Lesen ihrer Inhalte
        with open(file_name, mode="r", encoding="utf-8") as file:
            csv_reader = csv.reader(file)

            # Schleife durch jede Zeile der CSV-Datei
            for line in csv_reader:

                # Initialisierung eines internen NPs und Zaehlers
                internal_np = dict()
                np_id_number = line[0]
                data_count = 0

                # Extrahieren von Informationen aus der aktuellen Zeile
                basic_np = line[1]
                np_morpho_info = line[2:-1]
                sentence = line[-1]

                # Schleife durch die morphologischen Informationen fuer die NP
                for entry in np_morpho_info:
                    data_count += 1

                    # Aufspalten der Informationen in Nomen, Wortart (POS) und morphologische Merkmale
                    np_morpho_entry_data = entry.split()

                    np, pos, morpho_info = np_morpho_entry_data
                    congruency_info = morpho_info.split("|")

                    # Initialisierung eines Dictionaries fuer die Kongruenzinformationen
                    congru = dict()
                    congru["unk"] = []  # Unbekannte Merkmale

                    # Kategorisierung der Kongruenzinformationen
                    for info in congruency_info:
                        if info in number:
                            congru["numerus"] = info
                        elif info in gender:
                            congru["genus"] = info
                        elif info in case:
                            congru["kasus"] = info
                        elif info in article:
                            congru["def"] = info
                        else:
                            congru["unk"].append(info)

                    # Hinzufuegen der internen NP-Daten zum internen NP-Dictionary
                    internal_np[data_count] = {
                        "noun": np,
                        "pos": pos,
                        "noun_info": congru,
                    }

                # Zusammenfuehren der internen NP-Daten und Speichern im
                # Haupt-NP-Dictionary

                np_data[np_id_number] = {
                    "full_np": basic_np,
                    "sentence": sentence,
                } | internal_np

        # Rueckgabe des gesammelten NP-Dictionaries
        return np_data

    def get_read_in_lemmas(self) -> list:
        """
        Diese Methode liest Lemmata aus einer Datei und gibt sie als Liste zurueck.

        Returns:
            lemmas (list): Eine Liste von Lemmata, ohne Zeilenumbrueche.
        """
        with open(self.lemma_txt, mode="r", encoding="utf-8") as file:
            lemmas = [lemma.replace("\n", "") for lemma in file.readlines()]
            return lemmas


if __name__ == "__main__":
    pass
