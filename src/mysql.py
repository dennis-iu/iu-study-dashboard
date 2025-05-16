from src.db_base import DbBase


class MySqlDb(DbBase):
    """Klasse für die MySQL-Datenbankanbindung."""

    def __init__(self, config):
        """
        Initialisierung der MySqlDb-Klasse.

        :param config: dict - Konfigurationsdatei
        :return: None
        """
        super().__init__(config)
        self.host = self.config["mysql"]["host"]
        self.port = self.config["mysql"]["port"]
        self.database = self.config["mysql"]["database"]
        self.user = self.config["mysql"]["user"]
        self.password = self.config["mysql"]["password"]

    def connect(self):
        """Verbindungsaufbau zur MySQL-Datenbank."""
        import mysql.connector

        self.connection = mysql.connector.connect(
            host=self.host,
            port=self.port,
            database=self.database,
            user=self.user,
            password=self.password,
        )
        return self.connection

    def disconnect(self):
        """Verbindung zur MySQL-Datenbank schließen."""
        if self.connection:
            self.connection.close()
            self.connection = None

    def execute_query(self, query):
        """
        Ausführen einer SQL-Abfrage.

        :param query: str - SQL-Abfrage
        :return: list - Ergebnis der Abfrage
        """
        cursor = self.connection.cursor()
        cursor.execute(query)

        if query.strip().lower().startswith(("insert", "update", "delete")):
            self.connection.commit()
            result = []
        else:
            result = cursor.fetchall()

        cursor.close()
        return result
