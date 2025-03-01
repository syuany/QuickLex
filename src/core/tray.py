from PyQt5.QtWidgets import QSystemTrayIcon, QMenu, QApplication
from PyQt5.QtGui import QIcon


class TrayIcon(QSystemTrayIcon):
    def __init__(self, main_window, icon_path):
        super().__init__()
        self.main_window = main_window
        self.init_tray(icon_path)

    def init_tray(self, icon_path):
        self.setIcon(QIcon(icon_path))
        menu = QMenu()

        toggle_action = menu.addAction("显示/隐藏窗口")
        toggle_action.triggered.connect(self.main_window.toggle_visibility)

        menu.addSeparator()

        exit_action = menu.addAction("退出")
        exit_action.triggered.connect(self.cleanup_exit)

        self.setContextMenu(menu)

    def cleanup_exit(self):
        self.setVisible(False)
        QApplication.quit()
