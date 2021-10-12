"""Provides QtWebEngineCore classes and functions."""

from prettyqt.qt import PYQT5, PYQT6, PYSIDE2, PYSIDE6, PythonQtError


if PYQT5:
    from PyQt5.QtWebEngineCore import *
    from PyQt5.QtWebEngineWidgets import (
        QWebEngineHistory,
        QWebEngineHistoryItem,
        QWebEngineScript,
        QWebEngineScriptCollection,
        QWebEngineProfile,
        QWebEngineSettings,
        QWebEnginePage,
        QWebEngineDownloadItem as QWebEngineDownloadRequest,
        QWebEngineContextMenuData as QWebEngineContextMenuRequest,
    )
elif PYSIDE2:
    from PySide2.QtWebEngineCore import *
    from PySide2.QtWebEngineWidgets import (
        QWebEngineHistory,
        QWebEngineHistoryItem,
        QWebEngineScript,
        QWebEngineScriptCollection,
        QWebEngineProfile,
        QWebEngineSettings,
        QWebEnginePage,
        QWebEngineDownloadItem as QWebEngineDownloadRequest,
        QWebEngineContextMenuData as QWebEngineContextMenuRequest,
    )
elif PYQT6:
    from PyQt6.QtWebEngineCore import *
elif PYSIDE6:
    from PySide6.QtWebEngineCore import *
else:
    raise PythonQtError("No Qt bindings could be found")
