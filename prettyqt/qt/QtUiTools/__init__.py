"""Provides QtTest classes and functions."""

from prettyqt.qt import PYQT5, PYSIDE2, PYSIDE6, PythonQtError


if PYQT5:
    from PyQt5 import uic

    class QUiLoader:
        def load(self, path: str):
            return uic.loadUi(path)

    RCC_CMD = "pyrcc5 -no-compress"
    LUPDATE_CMD = "pylupdate5 -verbose"
    UIC_CMD = "pyuic5 --debug"
elif PYSIDE2:
    from PySide2.QtUiTools import QUiLoader, loadUiType

    RCC_CMD = "pyside2-rcc --no-compress --verbose"
    LUPDATE_CMD = "pyside2-lupdate -verbose"
    UIC_CMD = "pyside2-uic"
elif PYSIDE6:
    from PySide6.QtUiTools import QUiLoader, loadUiType  # type: ignore

    RCC_CMD = "pyside6-rcc --no-compress --verbose"
    LUPDATE_CMD = "pyside6-lupdate -verbose"
    UIC_CMD = "pyside6-uic"
else:
    raise PythonQtError("No Qt bindings could be found")
