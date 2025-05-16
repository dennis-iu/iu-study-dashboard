import importlib
from tkinter import PhotoImage

from ui.add import AddUi
from ui.change import ChangeUi
from ui.delete import DeleteUi
from ui.ui_base import UiBase


class SelectUi(UiBase):
    """Klasse für das Select-Dasboard."""

    def __init__(self, master, config):
        """
        Initialisierung der Select-Klasse.

        :param master: Tkinter Objekt
        :param config: dict - Konfigurationsdatei
        :return: None
        """
        super().__init__(master, config, "Course Changes")

        # Liste für die hintergrundbilder der Auswahlkarten erstellen
        self.selection_card_bg_images = []

        # Auswahlkarten erstellen
        self.create_selection_cards(
            150.0,
            300.0,
            "ADD COURSE",
            ["Leads to an input page", "for entering a new", "course"],
            AddUi,
        )
        self.create_selection_cards(
            400.0,
            300.0,
            "CHANGE STATUS",
            ["Gives you the", "opportunity to change", "course settings"],
            ChangeUi,
        )
        self.create_selection_cards(
            650.0,
            300.0,
            "DELETE COURSE",
            ["Leads to a selection", "page to delete the", "selected course"],
            DeleteUi,
        )

        # Zurück Button erstellen
        home_module = importlib.import_module(
            "ui.home"
        )  # Um Circular Import Probleme zu verhindern
        HomeUi = home_module.HomeUi
        self.create_button(
            "back", lambda: self.switch_to(HomeUi), {"x": 35.0, "y": 15.0}
        )

        self.window.mainloop()

    def create_selection_cards(
        self, image_x, image_y, card_title, card_desc, select_option
    ):
        """
        Erstellung der Auswahlkarten.

        :param image_x: int - x Position der Karte
        :param image_y: int - y Position der Karte
        :param card_title: str - Titel der Karte
        :param card_desc: list - Liste mit Beschreibungen für die Karte
        :param select_option: class - Klasse für die Auswahloption
        :return: None
        """
        # PhotoImage für die Auswahlkarten initialisieren
        selection_card_bg_image = PhotoImage(
            file=self.config["assets_path"] + "selection_card_bg.png"
        )
        img_height = selection_card_bg_image.height()
        self.selection_card_bg_images.append(selection_card_bg_image)

        # Auwahlkarten Hintergrund setzen
        selection_card_bg = self.canvas.create_image(
            image_x,
            image_y,
            image=selection_card_bg_image,
        )

        # Titel für die Auswahlkarten setzen
        self.create_dynamic_text(
            card_title,
            {"x": image_x, "y": image_y - img_height // 2 + 45},
            "Poppins ExtraBold",
            21 * -1,
            "center",
            "#FFFFFF",
            "bold",
        )

        # Beschreibung für die Auswahlkarten setzen
        desc_add = 85

        for desc in card_desc:
            self.create_dynamic_text(
                desc,
                {"x": image_x, "y": image_y - img_height // 2 + desc_add},
                "Inter Light",
                17 * -1,
                "center",
                "#FFFFFF",
            )
            desc_add += 30

        # Button für die Auswahlkarten setzen
        self.create_button(
            "arrow",
            lambda: self.switch_to(select_option),
            {"x": image_x, "y": image_y - img_height // 2 + 170},
        )
