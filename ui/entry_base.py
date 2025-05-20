import os
import sys

from ui.ui_base import UiBase

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from abc import abstractmethod
from tkinter import (Button, Canvas, Entry, Frame, Label, PhotoImage,
                     Radiobutton, Scrollbar, StringVar, Toplevel, messagebox)


class EntryBase(UiBase):
    """Base-Klasse für alle Entry-Dashboards."""

    @abstractmethod
    def specific_window(self):
        """Methode um das spezifische Fenster zu erstellen."""
        # Hier können spezifische Fenster erstellt werden

    def create_entry(self, name, position):
        """
        Methode um ein Eingabefenster im Canvas zu integrieren.

        :param name: str - Name des Eingabefeldes
        :param position: dict - Position des Entrys (z. B. {"x": 50.0, "y": 50.0, "width": 50.0, "height": 50.0})
        :return: None
        """
        entry_image = PhotoImage(file=self.config["assets_path"] + "entry_bar.png")
        entry_bg = self.canvas.create_image(450.5, 206.0, image=entry_image)
        entry = Entry(bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0)
        entry.place(**position)
        self.entries[name] = entry

    def create_dropdown(
        self, name, options, position, width=265, height=28, bg_color="#FFFFFF"
    ):
        """
        Methode, um ein Dropdown-Menü mit Scrollfunktion im Canvas zu integrieren.

        :param name: str - Name des Dropdowns
        :param options: list - Liste der Auswahlmöglichkeiten
        :param position: dict - Position des Dropdowns (z. B. {"x": 50.0, "y": 50.0})
        :param width: int - Breite des Dropdowns (Default - 265)
        :param height: int - Höhe des Dropdowns (Default - 28)
        :param bg_color: str - Hintergrundfarbe des Dropdowns (Default - weiß)
        :return: None
        """
        # Haupt-Label
        label_text = StringVar(value="Dropdown-Menü")

        label = Label(
            self.canvas,
            textvariable=label_text,
            bg=bg_color,
            relief="flat",
            highlightbackground="#CCCCCC",
            highlightthickness=2,
        )
        label.place(x=position["x"], y=position["y"], width=width, height=height)

        # Speichere Optionen und Status
        selected_var = StringVar()
        self.dropdown_references[name] = {
            "label": label,
            "options": options,
            "selected_var": selected_var,
        }

        # Dropdown anzeigen
        def show_dropdown(event):
            current_ref = self.dropdown_references[name]
            if "window" in current_ref and current_ref["window"] is not None:
                current_ref["window"].destroy()

            dropdown_window = Toplevel()
            dropdown_window.overrideredirect(True)
            dropdown_window.configure(bg=bg_color)

            # Position berechnen
            x = event.x_root
            y = event.y_root + height

            screen_height = dropdown_window.winfo_screenheight()
            dropdown_height = min(300, len(options) * 30 + 50)

            if y + dropdown_height > screen_height:
                y = event.y_root - dropdown_height

            dropdown_window.geometry(
                f"{int(width)}x{int(dropdown_height)}+{int(x)}+{int(y)}"
            )
            dropdown_window.focus_set()

            def close_dropdown_delayed(event):
                dropdown_window.after(100, lambda: dropdown_window.destroy())

            dropdown_window.bind("<FocusOut>", lambda e: close_dropdown_delayed())

            # Canvas mit Scrollbar für Optionen
            container = Frame(dropdown_window, bg=bg_color)
            container.pack(fill="both", expand=True)

            canvas = Canvas(container, bg=bg_color, highlightthickness=0)
            scrollbar = Scrollbar(container, orient="vertical", command=canvas.yview)
            scrollable_frame = Frame(canvas, bg=bg_color)

            scrollable_frame.bind(
                "<Configure>",
                lambda e: canvas.configure(scrollregion=canvas.bbox("all")),
            )

            canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
            canvas.configure(yscrollcommand=scrollbar.set)

            canvas.pack(side="left", fill="both", expand=True)
            scrollbar.pack(side="right", fill="y")

            # Auswahl + Label-Update
            def update_label():
                selected_value = selected_var.get()
                label_text.set(selected_value if selected_value else "Dropdown-Menü")

            for option in current_ref["options"]:
                Radiobutton(
                    scrollable_frame,
                    text=option,
                    variable=selected_var,
                    value=option,
                    bg=bg_color,
                    anchor="w",
                    command=update_label,
                ).pack(fill="x", padx=5, pady=2)

            # OK-Button
            Button(
                scrollable_frame,
                text="OK",
                command=dropdown_window.destroy,
                bg=bg_color,
            ).pack(fill="x", padx=5, pady=5)

            current_ref["window"] = dropdown_window
            setattr(self, f"{name}_dropdown_window", dropdown_window)

        # Klick auf Label öffnet Dropdown
        label.bind("<Button-1>", show_dropdown)

    def get_selected_dropdown_value(self, name):
        """
        Methode um den ausgewählten Wert aus dem Dropdown-Menü zu erhalten.

        :param name: str - Name des Dropdowns
        :return: str - Ausgewählter Wert
        """
        ref = self.dropdown_references.get(name)
        if not ref:
            return ""
        return ref["selected_var"].get()

    def check_grade_entry(self, status, grade):
        """
        Methode um zu überprüfen, ob die Note richtig eingegeben wurde.

        :param status: str - Status des Kurses
        :param grade: str - Note des Kurses
        :return: bool - True wenn die Note eingegeben werden kann, sonst False
        """
        if grade == "" and status != "completed":
            return "NULL"
        elif grade == "" and status == "completed":
            self.show_error_dialog("Grade must be set if the course is completed.")
            return "NULL"
        elif grade != "" and status != "completed":
            self.show_error_dialog("Grade can only be set if the course is completed.")
            return "NULL"
        elif grade != "" and status == "completed":
            grade = float(grade)
            if grade < 0.0 or grade > 6.0:
                self.show_error_dialog("Grade must be between 0.0 and 6.0.")
                return "NULL"
        return grade

    def show_info_dialog(self, message):
        """
        Methode um die Info-Nachricht anzuzeigen

        :param path: str - Info-Nachricht
        :return: None
        """
        messagebox.showinfo("Info", message)

    def show_error_dialog(self, message):
        """
        Methode um die Error-Nachricht anzuzeigen

        :param path: str - Error-Nachricht
        :return: None
        """
        messagebox.showerror("Fehler", message)
