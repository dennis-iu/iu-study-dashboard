import importlib
import logging as log

from ui.ui_base import UiBase


class AddUi(UiBase):
    """Klasse für das Add-Dasboard."""

    def __init__(self, master, config):
        """
        Initialisierung der Add-Klasse.

        :param master: Tkinter Objekt
        :param config: dict - Konfigurationsdatei
        :return: None
        """
        super().__init__(master, config, "Add Course")

        # Eingabefelder für Kursinformationen erstellen
        entry_fields = [
            "Course ID",
            "Course Name",
            "Course Status",
            "Tutors",
            "ECTs",
            "Grade (optional)",
        ]
        options = {"Course Status": ["open", "in progress", "completed"]}
        y_pos = 125.0
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
            if field == "Course Status":
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
            y_pos += 65.0

        # Submit Button erstellen
        self.create_button(
            "submit", lambda: self.add_course(), {"x": 400.0, "y": 507.0}
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

    def add_course(self):
        """Funktion zum Hinzufügen eines neuen Kurses."""
        # Kursinformationen aus den Eingabefeldern abrufen
        try:
            course_id = self.entries["Course ID"].get()
            course_name = self.entries["Course Name"].get()
            course_status = self.get_selected_dropdown_value("Course Status")
            tutors = self.entries["Tutors"].get()
            ects = self.entries["ECTs"].get()
            if ects != "":
                ects = int(ects)
                if ects < 0 or ects > 180:
                    self.show_error_dialog("Ects must be between 0 and 180.")
            grade = self.check_grade_entry(
                course_status, self.entries["Grade (optional)"].get()
            )

            # Überprüfen, ob alle Pflicht-Eingabefelder ausgefüllt sind
            if not all([course_id, course_name, course_status, tutors, ects]):
                raise ValueError("All fields must be filled.")
        except Exception as e:
            self.show_error_dialog(e)
            return

        # Variablen in ein SQL-Statement schreiben
        insert = f"INSERT INTO courses (course_id, course_name, course_status, tutors, ects, grade)"
        values = f"VALUES ('{course_id}', '{course_name}', '{course_status}', '{tutors}', {ects}, {grade})"

        sql = f"{insert} {values}"
        log.debug(f"SQL-Statement: {sql}")
