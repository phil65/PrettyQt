from __future__ import annotations

from prettyqt import gui


class Bitmap(gui.PixmapMixin, gui.QBitmap):
    """Monochrome (1-bit depth) pixmaps."""


if __name__ == "__main__":
    app = gui.app()
    image = Bitmap()
    bytes(image)
