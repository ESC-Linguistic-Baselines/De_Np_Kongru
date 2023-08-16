# Standard
import os

# Pip
import yaml

# Custom
from kongru.api_general.universal.funcs.basic_logger import get_logger


def get_config_data(yaml_file: str = "config.yaml") -> dict:
    """
    Liest Konfigurationsdaten aus einer YAML-Datei.

    Diese Funktion liest Konfigurationsdaten aus einer YAML-Datei mit dem angegebenen Dateinamen.
    Die Funktion verwendet die PyYAML-Bibliothek, um die Daten sicher zu laden.

    Args:
        yaml_file (str, optional): Der Name der YAML-Datei. Standardmäßig ist dies "yaml_config_file.yaml".

    Returns:
        dict: Ein Wörterbuch (Dictionary), das die geladenen Konfigurationsdaten enthaelt.

    Beispiel:
        Angenommen, die Datei "yaml_config_file.yaml" enthält die folgenden Daten:
        ```
        home_directory: /pfad/zum/home
        api_key: mein_api_schluessel
        ```
        Dann ruft der Aufruf der Funktion `get_config_data()` ein Wörterbuch (Dictionary) ab:
        ```
        {'home_directory': '/pfad/zum/home', 'api_key': 'mein_api_schluessel'}
        ```
    """
    try:
        with open(yaml_file) as config_file:
            yaml_config_file = yaml.safe_load(config_file)
            return yaml_config_file
    except Exception as e:
        logger = get_logger()
        custom_message = "Es sind Probleme mit der Yaml-Datei aufgetreten."
        logger.error(e, extra={"custom_message": custom_message})

