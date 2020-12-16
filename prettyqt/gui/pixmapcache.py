from typing import Dict, Optional

from qtpy import QtGui


class PixmapCache(QtGui.QPixmapCache):
    MAP: Dict[str, QtGui.QPixmapCache.Key] = dict()

    def __setitem__(self, key: str, value: QtGui.QPixmap):
        cache_key = self.insert(value)
        self.MAP[key] = cache_key

    def __getitem__(self, key: str) -> Optional[QtGui.QPixmap]:
        cache_key = self.MAP[key]
        return self.find(cache_key)

    def __delitem__(self, key: str):
        self.remove(key)


if __name__ == "__main__":
    from prettyqt import gui

    app = gui.app()
    cache = PixmapCache()
    pix = QtGui.QPixmap()
    cache["test"] = pix
    assert cache["test"] == pix
