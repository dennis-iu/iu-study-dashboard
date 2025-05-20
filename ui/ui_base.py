import logging as log
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from abc import ABC, abstractmethod
from tkinter import Canvas, PhotoImage


class UiBase(ABC):
    """Base-Klasse für alle Dashboards."""

    def __init__(self, master, config, db, window_title):
        """
        Initialisierung der UiBase-Klasse.

        :param master: Tkinter Objekt
        :param config: dict - Konfigurationsdatei
        :param db: class - Datenbankverbindung
        :param window_title: str - Titel des Fensters
        :return: None
        """
        # Variablen initialisieren
        self.window = master
        self.config = config
        self.mysqldb = db
        self.window_title = window_title
        self.entries = {}
        self.dropdown_references = {}

    def __enter__(self):
        """Initialisierung der UiBase-Klasse."""
        # Standard-Fenster erstellen
        self.standard_window()

        # Spezifisches Fenster erstellen
        self.specific_window()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Klasse verlassen / Schließen des Fensters.

        :param exc_type: Exception Type
        :param exc_val: Exception Value
        :param exc_tb: Exception Traceback
        :return: None
        """
        if self.window:
            self.window.destroy()
            log.info("Fenster geschlossen.")
        if exc_type is not None:
            log.error(f"Exception: {exc_type} - {exc_val}")
            log.error(
                f"Traceback: {exc_tb.tb_frame.f_code.co_filename} - {exc_tb.tb_lineno}"
            )
            raise exc_val

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

    @abstractmethod
    def specific_window(self):
        """Methode um das spezifische Fenster zu erstellen."""
        # Hier können spezifische Fenster erstellt werden

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
        with new_dashboard_class(self.window, self.config, self.mysqldb) as ndc:
            pass

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
