from qtpy import QtGui

from prettyqt import gui


QtGui.QRasterWindow.__bases__ = (gui.PaintDeviceWindow,)


class RasterWindow(QtGui.QRasterWindow):
    pass


if __name__ == "__main__":
    app = gui.GuiApplication([])
