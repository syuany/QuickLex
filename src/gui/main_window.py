from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import Qt


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.setup_close_behavior()

    def setup_close_behavior(self):
        self.closeEvent = lambda event: self.hide()

    def init_ui(self):
        self.setWindowTitle("QuickLex")
        self.setGeometry(800, 500, 400, 300)
        self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)

    def toggle_visibility(self):
        if self.isVisible():
            self.hide()
        else:
            self.showNormal()
            self.activateWindow()
            # self.raise_()
            # self.input_box.setFocus()
