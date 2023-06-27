from __future__ import annotations

from prettyqt import gui


class RasterWindow(gui.PaintDeviceWindowMixin, gui.QRasterWindow):
    pass


if __name__ == "__main__":
    app = gui.app()
