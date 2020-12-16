from qtpy import PYQT5, PYSIDE2


if PYQT5:
    from PyQt5 import QtWebEngineCore  # type: ignore
elif PYSIDE2:
    from PySide2 import QtWebEngineCore

from prettyqt import core


QtWebEngineCore.QWebEngineUrlSchemeHandler.__bases__ = (core.Object,)


class WebEngineUrlSchemeHandler(QtWebEngineCore.QWebEngineUrlSchemeHandler):
    pass


if __name__ == "__main__":
    item = WebEngineUrlSchemeHandler()
