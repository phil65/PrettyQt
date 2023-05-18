from __future__ import annotations

from collections import defaultdict
from collections.abc import Callable
import ctypes
from ctypes import WINFUNCTYPE, FormatError, c_bool, c_int
from ctypes.wintypes import UINT
import logging
from typing import SupportsInt

from prettyqt import core
from prettyqt.qt import QtCore
from prettyqt.utils.platforms.windows import keytables


logger = logging.getLogger(__name__)


class GlobalHotKeyEventFilter(core.AbstractNativeEventFilter):
    _keybindings = defaultdict(list)
    _keygrabs = defaultdict(int)  # Key grab key -> number of grabs

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user32 = ctypes.WinDLL("user32", use_errno=True, use_last_error=True)
        # msdn.microsoft.com/en-us/library/windows/desktop/ms646309%28v=vs.85%29.aspx
        prototype = WINFUNCTYPE(c_bool, c_int, c_int, UINT, UINT)
        paramflags = (1, "hWnd", 0), (1, "id", 0), (1, "fsModifiers", 0), (1, "vk", 0)
        self.RegisterHotKey = prototype(("RegisterHotKey", self.user32), paramflags)

        # msdn.microsoft.com/en-us/library/windows/desktop/ms646327%28v=vs.85%29.aspx
        prototype = WINFUNCTYPE(c_bool, c_int, c_int)
        paramflags = (1, "hWnd", 0), (1, "id", 0)
        self.UnregisterHotKey = prototype(("UnregisterHotKey", self.user32), paramflags)

    def nativeEventFilter(self, eventType, message):
        WM_HOTKEY_MSG = 0x0312  # 768
        msg = ctypes.wintypes.MSG.from_address(int(message))
        handled = False
        if eventType != b"windows_generic_MSG" or msg.message != WM_HOTKEY_MSG:
            return False, 0
        key = msg.lParam
        logger.info(f"handling hotkey {key}")
        for cb in self._keybindings.get(key, []):
            try:
                cb()
            finally:
                handled = True
        return handled, 0

    def register_hotkey(
        self,
        keycombo: QtCore.QKeyCombination,
        callback: Callable,
        wid: SupportsInt | None = None,
    ):
        wid = 0x0 if wid is None else int(wid)
        mods = keytables.qt_mod_to_virtual(keycombo.keyboardModifiers())
        kc = keytables.virtual_key_for_qtkey(keycombo.key())
        # High word = Key code, Low word = Modifiers
        # https://msdn.microsoft.com/en-us/library/windows/desktop/ms646279%28v=vs.85%29.aspx
        # Add MOD_NOREPEAT = 0x4000 to mods, so that keys don't get notified twice
        # This requires VISTA+ operating system
        key_index = kc << 16 | mods
        logger.info(f"registering key {key_index} for window {wid}")
        if not self._keygrabs[key_index] and not self.RegisterHotKey(
            wid, key_index, UINT(mods | 0x4000), UINT(kc)
        ):
            logger.warning("Couldn't register hot key!")
            return False

        self._keybindings[key_index].append(callback)
        self._keygrabs[key_index] += 1
        return True

    def unregister_hotkey(
        self, keycombo: QtCore.QKeyCombination, wid: SupportsInt | None = None
    ):
        wid = 0x0 if wid is None else int(wid)
        mods = keytables.qt_mod_to_virtual(keycombo.keyboardModifiers())
        kc = keytables.virtual_key_for_qtkey(keycombo.key())
        key_index = kc << 16 | mods

        self._keybindings.pop(key_index)
        self._keygrabs.pop(key_index)

        logger.info(f"unregistering key {key_index} for window {wid}")
        if not self.UnregisterHotKey(wid, key_index):
            err = f"Couldn't unregister hot key '{kc}': {FormatError()}."
            logger.error(err)
            return False
        return True


if __name__ == "__main__":
    import sys

    from prettyqt import gui, widgets

    app = widgets.app()
    window = widgets.MainWindow()
    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
    logger.info("\tPress Ctrl+Shift+A or Print Screen any where to trigger a callback.")
    logger.info("\tCtrl+Shift+F unregisters and re-registers previous callback.")
    logger.info("\tCtrl+Shift+E exits the app.")

    # Setup a global keyboard shortcut to logger.info "Hello World" on pressing
    # the shortcut
    win_event_filter = GlobalHotKeyEventFilter()

    def callback():
        logger.info("hello world")

    def exit_app():
        window.close()

    def unregister():
        combo = gui.KeySequence("Shift+Ctrl+A")[0]
        win_event_filter.unregister_hotkey(combo)
        logger.info("unregister and register previous binding")
        win_event_filter.register_hotkey(combo, callback)

    combo = gui.KeySequence("Shift+Ctrl+A")[0]
    win_event_filter.register_hotkey(combo, callback)
    combo = gui.KeySequence("Print Screen")[0]
    win_event_filter.register_hotkey(combo, callback)
    combo = gui.KeySequence("Shift+Ctrl+E")[0]
    win_event_filter.register_hotkey(combo, exit_app)
    combo = gui.KeySequence("Shift+Ctrl+F")[0]
    win_event_filter.register_hotkey(combo, unregister)

    # # Install a native event filter to receive events from the OS
    win_event_filter.install()

    window.show()
    app.exec()
    combo = gui.KeySequence("Shift+Ctrl+A")[0]
    win_event_filter.unregister_hotkey(combo)
    combo = gui.KeySequence("Shift+Ctrl+F")[0]
    win_event_filter.unregister_hotkey(combo)
    combo = gui.KeySequence("Shift+Ctrl+E")[0]
    win_event_filter.unregister_hotkey(combo)
