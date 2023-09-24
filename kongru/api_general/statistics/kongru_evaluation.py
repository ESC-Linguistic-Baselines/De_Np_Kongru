# Standard
import csv
import glob

import warnings

# Pip
import sklearn.exceptions
import typer

from sklearn.metrics import classification_report

# Custom

# generals
from kongru.api_general.universal.constants.general_vars import CODE_NAMES
from kongru.api_general.universal.constants.general_paths import GeneralPaths as Gp
from kongru.api_general.universal.constants.message_keys import MessageKeys as Mk
from kongru.api_general.universal.funcs.basic_logger import catch_and_log_error

statistics_keys = Mk.Statistics


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

    try:
        # Dateien aufstellen
        gold_files = [CODE_NAMES[code] for code in get_files(Gp.GOLD_FILES_GLOB.value)]
        raw_files = [CODE_NAMES[code] for code in get_files(Gp.RAW_FILES_GLOB.value)]

        # Ergebnisse
        with warnings.catch_warnings():
            # Wenn eine Klasse nicht berechnet werden kann, werden Divisionsfehler
            # von SKlearn ausgegeben. Diese werden hiermit unterdrueckt.
            warnings.filterwarnings(
                "ignore", category=sklearn.exceptions.UndefinedMetricWarning
            )
            classification_rep = classification_report(
                gold_files, raw_files, zero_division="warn"
            )
            typer.echo(classification_rep)
    except Exception as e:
        catch_and_log_error(
            echo_msg=True,
            error=e,
            custom_message=statistics_keys.GOLD_AND_RAW_FILES_INCORRECT.value,
        )


if __name__ == "__main__":
    pass
