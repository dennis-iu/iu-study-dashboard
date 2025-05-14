import logging as log

import yaml


def load_config(file_path):
    """
    Lädt die Konfiguration aus einer YAML-Datei.

    :param file_path: string - YAML-Dateipfad
    :return: dict
    """
    try:
        with open(file_path, "r") as file:
            return yaml.safe_load(file)
    except yaml.YAMLError as e:
        log.warning(f"Konfiguration konnte nicht geladen werden: {e}")
