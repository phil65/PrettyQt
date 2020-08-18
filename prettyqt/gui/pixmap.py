# -*- coding: utf-8 -*-

import pathlib
from typing import Union

from qtpy import QtGui

from prettyqt import gui, core


QtGui.QPixmap.__bases__ = (gui.PaintDevice,)


class Pixmap(QtGui.QPixmap):
    def __bool__(self):
        return not self.isNull()

    def __getstate__(self):
        return core.DataStream.create_bytearray(self)

    def __setstate__(self, ba):
        self.__init__()
        core.DataStream.write_bytearray(ba, self)

    @classmethod
    def from_file(cls, path: Union[pathlib.Path, str]):
        if isinstance(path, str):
            path = pathlib.Path(path)
        with path.open(mode="rb") as f:
            data = f.read()
        # Create widget
        pixmap = cls()
        pixmap.loadFromData(data)
        return pixmap


if __name__ == "__main__":
    from prettyqt import widgets

    app = widgets.app()
    p = Pixmap()
    print(bool(p))
