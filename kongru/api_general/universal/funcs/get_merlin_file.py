# Standard

# Pip
# None

# api_general
# Custom
from kongru.api_general.universal.funcs.basic_logger import catch_and_log_error


def open_merlin_file(
    data: dict,
    text_id: str,
    file_ending=".txt",
) -> str:
    """
    oeffnet eine Datei basierend auf den uebergebenen Daten und gibt ihren Inhalt zurueck.

    Args:
        data (dict): Ein dict von Daten, in dem die Dateiinformationen gefunden werden.
        text_id (str): Die ID des Texts, dessen Datei geoeffnet werden soll.
        file_ending (str, optional): Die Dateiendung (Standardmaeßig ".txt").

    Returns:
        str: Der Inhalt der geoeffneten Datei als Zeichenfolge (String).
    """
    file_raw_data = data.get(f"{text_id}.{file_ending}")

    if file_raw_data:
        try:
            with open(file_raw_data, mode="r", encoding="utf-8-sig") as outgoing_file:
                return outgoing_file.read()
        except Exception as e:
            catch_and_log_error(
                error=e,
                custom_message=f"Die Datei {file_raw_data} konnte nicht eingelesen "
                f"werden.",
                echo_msg=False,
            )
            return ""


if __name__ == "__main__":
    pass
