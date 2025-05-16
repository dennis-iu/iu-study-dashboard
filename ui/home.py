from tkinter import PhotoImage

from ui.select import SelectUi
from ui.ui_base import UiBase


class HomeUi(UiBase):
    """Klasse für das Home-Dashboard."""

    def __init__(self, master, config):
        """
        Initialisierung der Home-Klasse.

        :param master: Tkinter Objekt
        :param config: dict - Konfigurationsdatei
        :return: None
        """
        super().__init__(master, config, "Study Dashboard")

        # Liste für die hintergrundbilder der Statuskarten erstellen
        self.status_card_bg_images = []

        # Obere Statuskarten erstellen
        self.create_status_cards(400.0, 180.0, "grade average", "grade")

        # Untere Statuskarten erstellen
        self.create_status_cards(195.0, 388.0, "completed", "course")
        self.create_status_cards(400.0, 388.0, "in progress", "course")
        self.create_status_cards(605.0, 388.0, "open", "course")

        # course changes button erstellen
        self.create_button(
            "course_changes", lambda: self.switch_to(SelectUi), {"x": 400.0, "y": 507.0}
        )

        self.window.mainloop()

    def create_status_cards(self, image_x, image_y, card_title, card_type):
        """
        Erstellung der Statuskarten.

        :param image_x: int - x Position der Karte
        :param image_y: int - y Position der Karte
        :param card_title: str - Titel der Karte
        :param card_type: str - Typ der Karte (grade, course)
        :return: None
        """
        # PhotoImage für die Statuskarten initialisieren
        status_card_bg_image = PhotoImage(
            file=self.config["assets_path"] + "status_card_bg.png"
        )
        img_height = status_card_bg_image.height()
        self.status_card_bg_images.append(status_card_bg_image)

        # Statuskarten Hintergrund setzen
        status_card_bg = self.canvas.create_image(
            image_x,
            image_y,
            image=status_card_bg_image,
        )

        # Titel für die Statuskarten setzen
        self.create_dynamic_text(
            card_title,
            {"x": image_x, "y": image_y - img_height // 2 + 85},
            "Inter SemiBold",
            20 * -1,
            "center",
            "#4138D0",
        )

        # Labels für die Statuskarten setzen
        if card_type == "grade":
            # Symbolbild setzen
            self.grade_card_symbol_image = PhotoImage(
                file=self.config["assets_path"] + "grade_card_symbol.png"
            )
            self.grade_card_symbol = self.canvas.create_image(
                image_x,
                image_y - img_height // 2 + 33,
                image=self.grade_card_symbol_image,
                anchor="center",
            )
            # Textvariablen setzen
            values = [
                ("2.7 Ø", image_x - 50, image_y - img_height // 2 + 147),
                ("State", image_x - 55, image_y - img_height // 2 + 169),
                ("1.5 Ø", image_x + 50, image_y - img_height // 2 + 147),
                ("Target", image_x + 55, image_y - img_height // 2 + 169),
            ]

        if card_type == "course":
            # Kursanzahl setzen
            noc = 10
            self.create_dynamic_text(
                noc,
                {"x": image_x, "y": image_y - img_height // 2 + 33},
                "Inter Medium",
                20 * -1,
                "center",
            )
            # Textvariablen setzen
            values = [
                ("5 ECTs", image_x - 50, image_y - img_height // 2 + 147),
                ("State", image_x - 55, image_y - img_height // 2 + 169),
                ("180 ECTs", image_x + 50, image_y - img_height // 2 + 147),
                ("Total", image_x + 55, image_y - img_height // 2 + 169),
            ]

        # Text Labels setzen
        for text, x, y in values:
            self.create_dynamic_text(
                text, {"x": x, "y": y}, "Inter", 12 * -1, "center", "#787878"
            )

        # Parameter für die Statusleiste
        bar_width = 155
        bar_height = 6
        bar_radius = 6
        progress_percent = 0.65

        # Position der Statusleiste
        bar_x1 = image_x - 75
        bar_y1 = image_y + 52
        bar_x2 = bar_x1 + bar_width
        bar_y2 = bar_y1 + bar_height

        # Status Bar erstellen
        self.outer_status_bar = self.create_rounded_rectangle(
            x1=bar_x1,
            y1=bar_y1,
            x2=bar_x2,
            y2=bar_y2,
            radius=bar_radius,
            fill="#D2D2D2",
            outline="",
        )

        # Progress Part erstellen
        progress_width = bar_width * progress_percent
        self.progress_part = self.create_rounded_rectangle(
            x1=bar_x1,
            y1=bar_y1,
            x2=bar_x1 + progress_width,
            y2=bar_y2,
            radius=bar_radius,
            fill="#554CE1",
            outline="",
        )
