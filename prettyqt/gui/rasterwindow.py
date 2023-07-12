from __future__ import annotations

from prettyqt import gui


class RasterWindow(gui.PaintDeviceWindowMixin, gui.QRasterWindow):
    """Convenience class for using QPainter on a QWindow."""


if __name__ == "__main__":
    app = gui.app()
