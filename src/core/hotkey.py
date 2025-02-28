import win32con
import win32gui
from PyQt5.QtCore import QAbstractNativeEventFilter, QTimer
import ctypes


class HotkeyManager(QAbstractNativeEventFilter):
    def __init__(self, window):
        super().__init__()
        self.window = window
        self.hotkey_id = 1
        self.registered = False

    def register_hotkey(
        # self, modifiers=win32con.MOD_ALT | win32con.MOD_CONTROL, key=ord("D")
        self,
        modifiers=win32con.MOD_CONTROL,
        key=ord("1"),
    ):
        if not self.registered:
            try:
                win32gui.RegisterHotKey(None, self.hotkey_id, modifiers, key)
                self.registered = True
                # print(f"Hotkey registered successfully: {modifiers}, {key}")
            except Exception as e:
                print(f"Failed: register hotkey:{str(e)}")
                self.registered = False

    def nativeEventFilter(self, event_type, message):
        if event_type == "windows_generic_MSG":
            msg = ctypes.wintypes.MSG.from_address(message.__int__())
            if msg.message == win32con.WM_HOTKEY:
                if msg.wParam == self.hotkey_id:
                    # print("Hotkey triggered!")  # 调试信息
                    QTimer.singleShot(0, self.window.toggle_visibility)
                    return True, 0
        return False, 0
