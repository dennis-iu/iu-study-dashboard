import importlib
import logging as log

from ui.entry_base import EntryBase


class DeleteUi(EntryBase):
    """Klasse für das Delete-Dasboard."""

    def __init__(self, master, config, db):
        """
        Initialisierung der Delete-Klasse.

        :param master: Tkinter Objekt
        :param config: dict - Konfigurationsdatei
        :param db: class - Datenbankverbindung
        :return: None
        """
        super().__init__(master, config, db, "Delete Course")

    def specific_window(self):
        """Funktion zur Erstellung des spezifischen Fensters."""
        # Variablen für Eingabefeld
        field = "Select Course"
        options = {
            "Select Course": self.mysqldb.execute_query("select course_id from courses")
        }
        y_pos = 210.0
        x_pos = 190.0

        # Label erstellen
        self.create_dynamic_text(
            field,
            {"x": x_pos, "y": y_pos - 25},
            "Inter light",
            18 * -1,
            "nw",
            "#4138D0",
            "bold",
        )

        # Dropdown für Kursauswahl erstellen
        self.create_dropdown(
            name=field,
            options=options[field],
            position={"x": x_pos, "y": y_pos},
            width=420.0,
            height=30.0,
        )

        # Submit Button erstellen
        self.create_button(
            "submit", lambda: self.delete_course(), {"x": 400.0, "y": 507.0}
        )

        # Zurück Button erstellen
        select_module = importlib.import_module(
            "ui.select"
        )  # Um Circular Import Probleme zu verhindern
        SelectUi = select_module.SelectUi
        self.create_button(
            "back", lambda: self.switch_to(SelectUi), {"x": 35.0, "y": 15.0}
        )

        self.window.mainloop()

    def delete_course(self):
        """Funktion zum Löschen eines Kurses."""
        log.info("Deleting a course...")
        try:
            select_course = self.get_selected_dropdown_value("Select Course")

            # prüfen ob ein Kurs ausgewählt wurde
            if select_course == "":
                self.show_error_dialog("Please select a course to delete.")
        except Exception as e:
            self.show_error_dialog(e)

        # Variable in ein SQL-Statement schreiben
        delete = "DELETE FROM courses"
        where = f"WHERE course_id = '{select_course}'"

        sql = f"{delete} {where}"
        log.debug(f"SQL-Statement: {sql}")

        # SQL-Statement ausführen
        try:
            self.mysqldb.execute_query(sql)
            self.show_info_dialog(f"Course {select_course} deleted successfully.")
        except Exception as e:
            self.show_error_dialog(f"Error deleting course: {e}")
