from qtpy import QtGui

from prettyqt import gui


QtGui.QBitmap.__bases__ = (gui.Pixmap,)


class Bitmap(QtGui.QBitmap):
    pass


if __name__ == "__main__":
    app = gui.app()
    image = Bitmap()
    bytes(image)
