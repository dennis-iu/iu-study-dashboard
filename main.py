import logging as log
import os

from src.utils import load_config
from ui.home import HomeUi

try:
    import tkinter as tk
except ImportError:
    raise ImportError("tkinter nicht installiert.")

# log-config
log.basicConfig(
    level=log.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)


def main():
    """Main-Funktion um das Dashboard zu starten."""
    # Konfiguration laden
    config_path = "config/settings.yml"
    config = load_config(config_path)
    log.info("Konfig geladen!")

    # Konfiguration um assets_path erweitern
    assets_path = str(os.path.join(os.getcwd(), "ui/assets/"))
    config.update({"assets_path": assets_path})

    # Tkinter root initialisieren
    root = tk.Tk()

    # Root-Titel setzen
    root.title("study-dashboard")

    # Home Dashboard starten
    with HomeUi(root, config):
        log.info("Dashboard gestartet!")

    root.mainloop()


if __name__ == "__main__":
    main()
