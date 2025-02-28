import sys
from PyQt5.QtWidgets import QApplication
from gui.main_window import MainWindow
from core.tray import TrayIcon

import os


def main():
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)

    # Windows平台图标修复
    # if sys.platform == "win32":
    #     import ctypes
    #     ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("dictapp")

    window = MainWindow()

    icon_path = r"E:\workspace\class_101\QuickLex\resources\icon.png"
    tray = TrayIcon(window, icon_path)
    tray.show()

    window.show()
    # window.hide()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
