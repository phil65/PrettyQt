"""Classes for peer-to-peer communication between a server and HTML/JavaScript clients."""

import logging


logger = logging.getLogger(__name__)

try:
    from prettyqt.qt.QtWebChannel import *  # noqa: F403

    from .webchannel import WebChannel
    from prettyqt.qt import QtWebChannel

    QT_MODULE = QtWebChannel

    __all__ = ["WebChannel"]
except ModuleNotFoundError:
    logger.warning("Tried to import WebChannel module but not installed.")
