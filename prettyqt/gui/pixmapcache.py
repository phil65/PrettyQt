# from typing import Dict, Optional
from __future__ import annotations

from prettyqt.qt import QtGui


class PixmapCache(QtGui.QPixmapCache):
    pass
    # MAP: Dict[str, QtGui.QPixmapCache.Key] = {}

    # def __setitem__(self, key: str, value: QtGui.QPixmap):
    #     cache_key = self.insert(value)
    #     self.MAP[key] = cache_key

    # def __getitem__(self, key: str) -> Optional[QtGui.QPixmap]:
    #     cache_key = self.MAP[key]
    #     pixmap = gui.Pixmap()
    #     return pixmap if self.find(cache_key, pixmap) else None

    # def __delitem__(self, key: str):
    #     self.remove(key)


if __name__ == "__main__":
    from prettyqt import gui

    app = gui.app()
    cache = PixmapCache()
    pix = QtGui.QPixmap()
    cache["test"] = pix
    assert cache["test"] == pix
