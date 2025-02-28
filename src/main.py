import sys
from PyQt5.QtWidgets import QApplication
from gui.main_window import MainWindow
from core.tray import TrayIcon
from core.hotkey import HotkeyManager


def main():
    # 创建QApplication实例并设置退出行为
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)

    # Windows平台图标修复
    # if sys.platform == "win32":
    #     import ctypes
    #     ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("dictapp")

    # 创建主窗口实例
    window = MainWindow()

    # 设置托盘图标路径并创建托盘图标实例
    icon_path = r"E:\workspace\class_101\QuickLex\resources\icon.png"
    tray = TrayIcon(window, icon_path)

    # 创建热键管理器实例并注册热键
    hotkey = HotkeyManager(window)
    app.installNativeEventFilter(hotkey)
    hotkey.register_hotkey()

    # 显示托盘图标和主窗口
    tray.show()
    window.show()
    # window.hide()

    # 进入应用程序主循环
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
