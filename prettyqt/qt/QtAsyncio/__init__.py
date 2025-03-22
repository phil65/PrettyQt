"""Provides QtAsyncio classes and functions."""

from prettyqt.qt import PYSIDE6


if PYSIDE6:
    from PySide6.QtAsyncio import *  # noqa: F403  # type: ignore
else:
    msg = "No Qt bindings could be found"
    raise ModuleNotFoundError(msg)
