import logging as log
from abc import ABC, abstractmethod


class DbBase(ABC):
    """Base-Klasse für alle Datenbank-Anbindungen."""

    def __init__(self, config):
        """
        Initialisierung der DbBase-Klasse.

        :param config: dict - Konfigurationsdatei
        :return: None
        """
        # Variablen initialisieren
        self.config = config
        self.connection = None

    def __enter__(self):
        """Initialisierung der Datenbankverbindung."""
        self.connection = self.connect()
        log.info("Datenbankverbindung hergestellt.")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Klasse verlassen / Schließen der Datenbankverbindung.

        :param exc_type: Exception Type
        :param exc_val: Exception Value
        :param exc_tb: Exception Traceback
        :return: None
        """
        if self.connection:
            self.disconnect()
            log.info("Datenbankverbindung geschlossen.")
        if exc_type is not None:
            log.error(f"Exception: {exc_type} - {exc_val}")
            log.error(
                f"Traceback: {exc_tb.tb_frame.f_code.co_filename} - {exc_tb.tb_lineno}"
            )
            raise exc_val

    @abstractmethod
    def connect(self):
        """Verbindungsaufbau zur Datenbank."""
        # Implementierung der Verbindung zur Datenbank

    @abstractmethod
    def disconnect(self):
        """Verbindung zur Datenbank schließen."""
        # Implementierung der Trennung der Datenbankverbindung
