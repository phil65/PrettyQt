"""Webenginewidgets module.

contains QtWebEngineWidgets-based classes
"""

import logging


logger = logging.getLogger(__name__)

try:
    from prettyqt.qt.QtWebEngineWidgets import *  # noqa: F403

    from .webengineview import WebEngineView
    from prettyqt.qt import QtWebEngineWidgets

    QT_MODULE = QtWebEngineWidgets
    __all__ = [
        "WebEngineView",
    ]
except ModuleNotFoundError:
    logger.warning("Tried to import WebEngine module but not installed.")
