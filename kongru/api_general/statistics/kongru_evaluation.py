# Standard
import csv
import glob

import typer

# Pip
from sklearn.metrics import classification_report

# Custom

# generals
from kongru.api_general.universal.constants.general_vars import CODE_NAMES
from kongru.api_general.universal.constants.general_paths import GeneralPaths as Gp


def get_files(dataset: list[str]) -> list:
    """
    Diese Funktion liest CSV-Dateien aus einem gegebenen Datensatz und gibt die Inhalte als Liste zurück.

    Args:
        dataset (list[str]): Eine Liste von Dateipfaden zu den CSV-Dateien.

    Returns:
        csv_reader_data(list): Eine Liste der Inhalte aus den CSV-Dateien.
    """

    csv_reader_objects = list()
    csv_reader_data = list()

    dataset = glob.glob(dataset)

    for data_row in dataset:
        reference_data = csv.reader(open(data_row, mode="r", encoding="utf-8"))
        csv_reader_objects.append(reference_data)

    for data_row in csv_reader_objects:
        get_values = [i[0] for i in list(data_row)]
        csv_reader_data.extend(get_values)

    return csv_reader_data


def get_report() -> None:
    """
    Diese Funktion liest Gold- und Rohdaten aus CSV-Dateien,
    erstellt eine Klassifikationsbericht
    und gibt diesen Bericht aus.

    Returns:
        None
    """

    # Dateien aufstellen
    gold_files = [CODE_NAMES[code] for code in get_files(Gp.GOLD_FILES.value)]
    raw_files = [CODE_NAMES[code] for code in get_files(Gp.RAW_FILES.value)]

    # Ergebnisse
    classification_rep = classification_report(gold_files, raw_files)
    typer.echo(classification_rep)


if __name__ == "__main__":
    pass
