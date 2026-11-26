from typing import TYPE_CHECKING

from prettyqt import gui


if TYPE_CHECKING:
    from prettyqt.qt import QtGui

    _PaintDeviceWindowBase = QtGui.QPaintDeviceWindow
else:
    _PaintDeviceWindowBase = object


class PaintDeviceWindowMixin(
    gui.WindowMixin, gui.PaintDeviceMixin, _PaintDeviceWindowBase
):
    pass


class PaintDeviceWindow(PaintDeviceWindowMixin, gui.QPaintDeviceWindow):
    pass


if __name__ == "__main__":
    window = PaintDeviceWindow()
