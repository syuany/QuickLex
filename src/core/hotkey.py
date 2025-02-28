import win32con
import win32gui
from PyQt5.QtCore import QAbstractNativeEventFilter, QTimer
import ctypes


class HotkeyManager(QAbstractNativeEventFilter):
    def __init__(self, window):
        # 初始化HotkeyManager，设置窗口和热键ID
        super().__init__()
        self.window = window
        self.hotkey_id = 1
        self.registered = False

    def register_hotkey(
        self,
        modifiers=win32con.MOD_CONTROL,
        key=ord("1"),
    ):
        # 注册热键，设置修饰键和键值
        if not self.registered:
            try:
                win32gui.RegisterHotKey(None, self.hotkey_id, modifiers, key)
                self.registered = True
            except Exception as e:
                print(f"Failed: register hotkey:{str(e)}")
                self.registered = False

    def nativeEventFilter(self, event_type, message):
        # 处理原生事件，检测热键触发
        if event_type == "windows_generic_MSG":
            msg = ctypes.wintypes.MSG.from_address(message.__int__())
            if msg.message == win32con.WM_HOTKEY:
                if msg.wParam == self.hotkey_id:
                    QTimer.singleShot(0, self.window.toggle_visibility)
                    return True, 0
        return False, 0
