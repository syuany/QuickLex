import sys
from PyQt5.QtWidgets import QApplication
from gui.main_window import MainWindow
from core.tray import TrayIcon
from core.hotkey import HotkeyManager
from core.utils import resource_path
import logging

logging.basicConfig(
    filename="debug.log",
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s] %(message)s",
)


def main():
    logging.info("Program start...")
    try:
        # 创建QApplication实例并设置退出行为
        app = QApplication(sys.argv)
        app.setQuitOnLastWindowClosed(False)

        # 创建主窗口实例
        window = MainWindow()

        # 设置托盘图标路径并创建托盘图标实例
        icon_path = resource_path("resources/icon.png")
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
    except Exception as e:
        logging.critical(f"fatal: {str(e)}", exc_info=True)


if __name__ == "__main__":
    main()
