import argparse
import sys
from pathlib import Path

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap, QAction
from PyQt6.QtWidgets import QApplication, QMainWindow, QFileDialog, QScrollArea, QMessageBox

from src.dialogs.dialog_config_settings import ConfigSettingsDialog
from src.dockwidgets.dockwidget_mapper_generator import MapperGeneratorDockwidget
from src.widgets.widget_image_selector import ImageSelectorWidget
from src.main_window import MainWindow
import logging
logger = logging.getLogger(__name__)


def main():
    parser = argparse.ArgumentParser(description="Simple DDNet Automapper")
    parser.add_argument("--image", type=Path, help="tileset image to load on startup")
    args = parser.parse_args()

    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    window.setWindowState(window.windowState() | Qt.WindowState.WindowMaximized)  # Maximize window

    if args.image:
        loaded = window.central_widget.loadImage(args.image)
        if not loaded:
            logger.warning(f"Could not load image '{args.image}'")

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
