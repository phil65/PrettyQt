"""Provides QtTest classes and functions."""

from prettyqt.qt import PYSIDE6, PythonQtError


if PYSIDE6:
    from PySide6.QtUiTools import QUiLoader, loadUiType  # type: ignore

    RCC_CMD = "pyside6-rcc --no-compress --verbose"
    LUPDATE_CMD = "pyside6-lupdate -verbose"
    UIC_CMD = "pyside6-uic"
else:
    raise PythonQtError("No Qt bindings could be found")
