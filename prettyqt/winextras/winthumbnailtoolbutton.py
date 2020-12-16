from qtpy import PYQT5, PYSIDE2


if PYQT5:
    from PyQt5 import QtWinExtras  # type: ignore
elif PYSIDE2:
    from PySide2 import QtWinExtras

from prettyqt import core


QtWinExtras.QWinThumbnailToolButton.__bases__ = (core.Object,)


class WinThumbnailToolButton(QtWinExtras.QWinThumbnailToolButton):
    pass


if __name__ == "__main__":
    from prettyqt import widgets

    app = widgets.app()
    btn = WinThumbnailToolButton()
    # app.main_loop()
