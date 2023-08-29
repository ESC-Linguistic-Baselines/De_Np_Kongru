# Standard
import os

# Pip
import yaml

# Custom
# None


def get_config_data(file: str = None) -> dict:
    """
    Liest Konfigurationsdaten aus einer YAML-Datei und gibt sie als
    Python-Datenstruktur zurueck.

    args:
    file(str) Der Dateipfad zur YAML-Konfigurationsdatei.
        Wenn nicht angegeben, wird die Standardkonfigurationsdatei 'config.yaml'
        im Verzeichnis des Skripts verwendet.

    :return
       config_data (dict): Ein Python-dict mit den Konfigurationsdaten.
    """
    if file is None:
        # Das Verzeichnis, in dem das Skript sich befindet
        script_verzeichnis = os.path.dirname(os.path.abspath(__file__))

        # der Pfad zur YAML-Konfigurationsdatei relativ zum Verzeichnis des Skripts
        file = os.path.join(script_verzeichnis, "main_config.yaml")

    # Lade die YAML-Konfigurationsdatei
    with open(file, "r") as config_file:
        config_data: dict = yaml.safe_load(config_file)

    return config_data


if __name__ == "__main__":
    pass
