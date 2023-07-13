"""Webenginewidgets module.

contains QtWebEngineCore-based classes
"""

import logging


logger = logging.getLogger(__name__)

try:
    from .webchannel import WebChannel
    from prettyqt.qt import QtWebChannel

    QT_MODULE = QtWebChannel

    __all__ = ["WebChannel"]
except ModuleNotFoundError:
    logger.warning("Tried to import WebEngine module but not installed.")
