import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from abc import ABC
from tkinter import (Button, Canvas, Entry, Label, PhotoImage, Radiobutton,
                     StringVar, Toplevel, messagebox)


class UiBase(ABC):
    """Base-Klasse für alle Dashboards."""

    def __init__(self, master, config, window_title):
        """
        Initialisierung der UiBase-Klasse.

        :param master: Tkinter Objekt
        :param config: dict - Konfigurationsdatei
        :param window_title: str - Titel des Fensters
        :return: None
        """
        # Variablen initialisieren
        self.config = config
        self.window = master
        self.window_title = window_title
        self.entries = {}
        self.dropdown_references = {}

        # Standard-Fenster erstellen
        self.standard_window()

    def standard_window(self):
        """Methode um das Standard-Fenster zu erstellen."""
        self.window.geometry("800x600")
        self.window.configure(bg="#DBDBDB")

        # Canvas initialisieren
        self.canvas = Canvas(
            self.window,
            bg="#DBDBDB",
            height=600,
            width=800,
            bd=0,
            highlightthickness=0,
            relief="ridge",
        )
        self.canvas.place(x=0, y=0)

        # Headline Balken erstellen
        self.headline_bar_image = PhotoImage(
            file=self.config["assets_path"] + "headline_bar.png"
        )
        self.headline_bar = self.canvas.create_image(
            400.0,
            43.0,
            image=self.headline_bar_image,
        )

        self.create_dynamic_text(
            self.window_title, {"x": 400.0, "y": 14.0}, "Inter SemiBold", 40 * -1, "n"
        )

    def switch_to(self, new_dashboard_class):
        """
        Methode um zu einem anderen Dashboard zu wechseln.

        :param new_dashboard_class: class - Dashboards zu dem gewechselt werden soll
        :return: None
        """
        # Altes Dashboard zurücksetzen
        for widget in self.window.winfo_children():
            widget.destroy()

        # Neues Dashboard laden
        new_dashboard_class(self.window, self.config)

    def create_rounded_rectangle(self, x1, y1, x2, y2, radius=10, **kwargs):
        """
        Methode um ein abgerundetes Rechteck im Canvas zu integrieren.

        :param x1: int - x1 Koordinate
        :param y1: int - y1 Koordinate
        :param x2: int - x2 Koordinate
        :param y2: int - y2 Koordinate
        :param radius: int - Radius der Ecken (Default - 10)
        :param kwargs: dict - Zusätzliche Parameter für die Canvas-Methode
        :return: None
        """
        points = [
            x1 + radius,
            y1,
            x1 + radius,
            y1,
            x2 - radius,
            y1,
            x2 - radius,
            y1,
            x2,
            y1,
            x2,
            y1 + radius,
            x2,
            y1 + radius,
            x2,
            y2 - radius,
            x2,
            y2 - radius,
            x2,
            y2,
            x2 - radius,
            y2,
            x2 - radius,
            y2,
            x1 + radius,
            y2,
            x1 + radius,
            y2,
            x1,
            y2,
            x1,
            y2 - radius,
            x1,
            y2 - radius,
            x1,
            y1 + radius,
            x1,
            y1 + radius,
            x1,
            y1,
        ]
        return self.canvas.create_polygon(points, smooth=True, **kwargs)

    def create_button(self, name, to_do, position, anchor="n"):
        """
        Methode um einen Button im Canvas zu integrieren.

        :param name: str - Name des Buttons (der Datei in Assets)
        :param to_do: function - Funktion die der Button ausführen soll
        :param position: dict - Position des Buttons (z. B. {"x": 50.0, "y": 50.0})
        :param anchor: str - Ausrichtung des Buttons (Default - center)
        :return: None
        """
        # Bilder laden
        button_image = PhotoImage(
            file=self.config["assets_path"] + "button_" + name + ".png"
        )

        button_image_hover = PhotoImage(
            file=self.config["assets_path"] + "button_hover_" + name + ".png"
        )

        # Button-Widget erstellen
        button = self.canvas.create_image(
            position["x"], position["y"], image=button_image, anchor=anchor
        )

        # Funktionen für Hover-Effekte
        def on_enter(event):
            """
            Funktion zum reagieren auf das hover event.

            :param event: event - enter event
            :return: None
            """
            self.canvas.itemconfig(button, image=button_image_hover)

        def on_leave(event):
            """
            Funktion zum reagieren auf das leave event.

            :param event: event - leave event
            :return: None
            """
            self.canvas.itemconfig(button, image=button_image)

        def on_click(event):
            """
            Funktion zum reagieren auf das click event.

            :param event: event - click event
            :return: None
            """
            to_do()

        # Event-Bindings
        self.canvas.tag_bind(button, "<Enter>", on_enter)
        self.canvas.tag_bind(button, "<Leave>", on_leave)
        self.canvas.tag_bind(button, "<Button-1>", on_click)

        # Speicher Bilder, damit sie nicht vom Garbage Collector gelöscht werden
        self.canvas.image_dict = getattr(self.canvas, "image_dict", {})
        self.canvas.image_dict[name] = (button_image, button_image_hover)

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
        Methode, um ein Dropdown-Menü im Canvas zu integrieren.

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
            """
            Methode um das Dropdown Menü basierend auf dem Event anzupassen.

            :param event: event - change event
            :return: None
            """
            current_ref = self.dropdown_references[name]
            if "window" in current_ref and current_ref["window"] is not None:
                current_ref["window"].destroy()

            dropdown_window = Toplevel()

            x = int(event.x_root)
            y = int(event.y_root + height)
            dropdown_window.geometry(f"+{x}+{y}")
            dropdown_window.overrideredirect(True)

            # Checkboxen hinzufügen
            def update_label():
                """Label aktualisieren."""
                selected_value = selected_var.get()
                label_text.set(selected_value if selected_value else "Dropdown-Menü")

            for option in current_ref["options"]:
                Radiobutton(
                    dropdown_window,
                    text=option,
                    variable=selected_var,
                    value=option,
                    bg=bg_color,
                    anchor="w",
                    command=update_label,
                ).pack(fill="x", padx=5, pady=2)

            # OK-Button zum Schließen
            def close_dropdown():
                """Dropdown schließen."""
                dropdown_window.destroy()
                current_ref["window"] = None

            Button(
                dropdown_window, text="Ok", command=close_dropdown, bg=bg_color
            ).pack(fill="x", padx=5, pady=5)

            # Speichern
            current_ref["window"] = dropdown_window

            setattr(self, f"{name}_dropdown_window", dropdown_window)

        # Label anklickbar machen
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

    def create_dynamic_text(
        self,
        input,
        position,
        font="Inter",
        fontsize=15 * -1,
        anchor="nw",
        fill="#FFFFFF",
        fontstyle="normal",
    ):
        """
        Funktion, um einen Text im Canvas zu integrieren.

        :param input: str - Eingabetext
        :param position: dict - Textposition ({"x": 50.0, "y": 50.0})
        :param font: str - Schriftart (Default - Inter)
        :param fontsize: int - Schriftgröße (Default - 15 * -1)
        :param anchor: str - Textausrichtung (Default - center)
        :param fill: str - Textfarbe (Default - white)
        :param fontstyle: str - Schriftstil (Default - normal)
        :return: None
        """
        self.canvas.create_text(
            position["x"],
            position["y"],
            anchor=anchor,
            text=input,
            fill=fill,
            font=(font, fontsize, fontstyle),
        )

    def check_grade_entry(self, status, grade):
        """
        Methode um zu überprüfen, ob die Note richtig eingegeben wurde.

        :param status: str - Status des Kurses
        :param grade: str - Note des Kurses
        :return: bool - True wenn die Note eingegeben werden kann, sonst False
        """
        if grade == "" and status != "completed":
            return ""
        elif grade == "" and status == "completed":
            self.show_error_dialog("Grade must be set if the course is completed.")
            return ""
        elif grade != "" and status != "completed":
            self.show_error_dialog("Grade can only be set if the course is completed.")
            return ""
        elif grade != "" and status == "completed":
            grade = float(grade)
            if grade < 0.0 or grade > 6.0:
                self.show_error_dialog("Grade must be between 0.0 and 6.0.")
                return ""
        return grade

    def show_error_dialog(self, message):
        """
        Methode um die Error-Nachricht anzuzeigen

        :param path: str - Error-Nachricht
        :return: None
        """
        messagebox.showerror("Fehler", message)
