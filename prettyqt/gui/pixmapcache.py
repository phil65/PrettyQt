from __future__ import annotations

from prettyqt.qt import QtGui


class PixmapCache(QtGui.QPixmapCache):
    """Application-wide cache for pixmaps."""

    def __setitem__(self, key: str, value: QtGui.QPixmap):
        self.insert(key, value)

    def __getitem__(self, key: str) -> QtGui.QPixmap | None:
        return self.find(key)

    def __delitem__(self, key: str):
        self.remove(key)


if __name__ == "__main__":
    from prettyqt import gui
    from prettyqt.qt import QtCore

    app = gui.app()
    cache = PixmapCache()
    pix = gui.Pixmap.create_char("a", 10)
    cache["test"] = pix
    test = cache["test"]

    ba = QtCore.QByteArray()
    stream = QtCore.QDataStream(ba, QtCore.QIODeviceBase.OpenModeFlag.WriteOnly)
    stream << test
    assert ba.data() == bytes(pix)
