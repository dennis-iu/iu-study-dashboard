import importlib
import logging as log

from ui.ui_base import UiBase


class ChangeUi(UiBase):
    """Klasse für das Change-Dasboard."""

    def __init__(self, master, config):
        """
        Initialisierung der Change-Klasse.

        :param master: Tkinter Objekt
        :param config: dict - Konfigurationsdatei
        :return: None
        """
        super().__init__(master, config, "Change Status")

        # Eingabefelder für Statusänderungen erstellen
        entry_fields = ["Select Course", "Set Status", "Set Grade (optional)"]
        options = {
            "Select Course": ["Course 1", "Course 2", "Course 3"],
            "Set Status": ["open", "in progress", "completed"],
        }
        y_pos = 175.0
        x_pos = 190.0
        for field in entry_fields:
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
            # Eingabefeld erstellen
            if field != "Set Grade (optional)":
                # Dropdown für den Kursstatus erstellen
                self.create_dropdown(
                    name=field,
                    options=options[field],
                    position={"x": x_pos, "y": y_pos},
                    width=420.0,
                    height=30.0,
                )
            else:
                # Eingabefeld für den Kurs erstellen
                self.create_entry(
                    field, {"x": x_pos, "y": y_pos, "width": 420.0, "height": 30.0}
                )
            if field == "Select Course":
                y_pos += 35.0
            y_pos += 65.0

        # Submit Button erstellen
        self.create_button(
            "submit", lambda: self.change_status(), {"x": 400.0, "y": 507.0}
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

    def change_status(self):
        """Funktion zum Ändern des Status eines Kurses."""
        try:
            select_course = self.get_selected_dropdown_value("Select Course")
            set_status = self.get_selected_dropdown_value("Set Status")
            set_grade = self.check_grade_entry(
                set_status, self.entries["Set Grade (optional)"].get()
            )

            # Überprüfen, ob alle Pflicht-Eingabefelder ausgefüllt sind
            if not all([select_course, set_status, set_grade]):
                raise ValueError("All fields must be filled.")
        except Exception as e:
            self.show_error_dialog(e)

        # Variablen in ein SQL-Statement schreiben
        update = "UPDATE courses"
        set = f"SET status = '{set_status}', grade = {set_grade} WHERE course_name = '{select_course}'"

        sql = f"{update} {set}"
        log.debug(f"SQL-Statement: {sql}")
