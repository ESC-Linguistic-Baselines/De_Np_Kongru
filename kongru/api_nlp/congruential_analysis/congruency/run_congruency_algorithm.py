# Standard
import os

from typing import Callable

# Pip
import typer

# Custom
from kongru.api_general.universal.funcs.basic_logger import catch_and_log_info


def run_batch_congruency(
    congruency_algo: Callable,
    np_files: list,
    text_id_numbers: list,
    text_limit: int = 0,
    all_texts: bool = False,
) -> None:
    """
    Hier wird die Hauptanalyse fuer mehrere Dateien ausgefuehrt.

    Args:
        congruency_algo (Callable): der Algorithmus, der die NPs verarbeiten soll.
        all_texts(bool): Alle Texte sollen analysiert werden.
        np_files(list): Die Dateien, die analysiert werden sollen.
        text_id_numbers(list): Die Text-Id-Nummer der Texte, die anaylsiert werden sollen.
        text_limit (int): Die Anzahl der Dateien, die analysiert werden sollen.

    Returns:
            None
    """
    # Np Kongruenz bestimmen und die Ergebnisse speichern
    count = 0
    for np_ext_file in np_files:

        # Text-Id aufstellen
        file_name = os.path.basename(np_ext_file)
        txt_id = file_name.replace(".csv", "")

        if txt_id in text_id_numbers:
            if all_texts and text_limit == 0:
                text_limit = len(text_id_numbers)
            elif count >= text_limit:
                break

            count += 1
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

            catch_and_log_info(
                f"Text-Id {txt_id}: " f"Führe Hauptanalyse durch...", echo_msg=True
            )

            congruency_algo(file_name=np_ext_file)

            catch_and_log_info(
                f"Text-Id {txt_id}: " f"Hauptanalyse abgeschlossen \n", echo_msg=True
            )

            if count == text_limit:
                catch_and_log_info(
                    f"Alle Texte wurden erfolgreich analysiert.", echo_msg=True
                )


if __name__ == "__main__":
    pass
