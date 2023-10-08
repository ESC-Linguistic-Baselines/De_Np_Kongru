# Standard
import os

# Pip
# None

# Custom
# None


def generate_abs_rel_path(file_data: list) -> dict:
    """
    Die Dateien werden eingelesen und dann gesplittet, sodass
    der Key der relative Pfade und der Schluessel der absolute Pfade

    Args:
        file_data (list): Die Pfade der Dateien

    Returns:
        outgoing_data (dict): die Pfade der eingelesen Dateien
    """
    outgoing_data = dict()

    for file in file_data:
        path_extension = os.path.basename(file)
        outgoing_data[path_extension] = file

    return outgoing_data


if __name__ == "__main__":
    file = (
        "/Users/christopherchandler/repo/Python/computerlinguistik/de_np_kongru/main_sql_commands.sql",
    )

    generate_abs_rel_path(file)
