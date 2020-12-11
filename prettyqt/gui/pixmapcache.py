from typing import Optional

from qtpy import QtGui


class PixmapCache(QtGui.QPixmapCache):
    def __setitem__(self, key: str, value: QtGui.QPixmap):
        self.insert(key, value)

    def __getitem__(self, key: str) -> Optional[QtGui.QPixmap]:
        return self.find(key)

    def __delitem__(self, key: str):
        self.remove(key)


if __name__ == "__main__":
    from prettyqt import gui

    app = gui.app()
    cache = PixmapCache()
    pix = QtGui.QPixmap()
    cache["test"] = pix
    assert cache["test"] == pix
