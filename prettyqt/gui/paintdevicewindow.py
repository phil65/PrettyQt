from __future__ import annotations

from prettyqt import gui


class PaintDeviceWindowMixin(gui.WindowMixin, gui.PaintDeviceMixin):
    pass


class PaintDeviceWindow(PaintDeviceWindowMixin, gui.QPaintDeviceWindow):
    pass


if __name__ == "__main__":
    window = PaintDeviceWindow()
