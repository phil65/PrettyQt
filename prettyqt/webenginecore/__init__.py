"""Classes and functions for embedding web content in applications."""

import logging

logger = logging.getLogger(__name__)

try:
    from prettyqt.qt.QtWebEngineCore import *  # noqa: F403

    from .webenginehistoryitem import WebEngineHistoryItem
    from .webenginehistory import WebEngineHistory
    from .webenginehttprequest import WebEngineHttpRequest
    from .webenginecontextmenurequest import WebEngineContextMenuRequest
    from .webenginedownloadrequest import WebEngineDownloadRequest
    from .webengineurlscheme import WebEngineUrlScheme
    from .webengineurlschemehandler import WebEngineUrlSchemeHandler
    from .webenginesettings import WebEngineSettings
    from .webenginepage import WebEnginePage
    from .webenginescript import WebEngineScript
    from .webenginescriptcollection import WebEngineScriptCollection
    from .webengineprofile import WebEngineProfile
    from prettyqt.qt import QtWebEngineCore

    QT_MODULE = QtWebEngineCore
    __all__ = [
        "WebEngineContextMenuRequest",
        "WebEngineDownloadRequest",
        "WebEngineHistory",
        "WebEngineHistoryItem",
        "WebEngineHttpRequest",
        "WebEnginePage",
        "WebEngineProfile",
        "WebEngineScript",
        "WebEngineScriptCollection",
        "WebEngineSettings",
        "WebEngineUrlScheme",
        "WebEngineUrlSchemeHandler",
    ]
except ModuleNotFoundError:
    logger.warning("Tried to import WebEngine module but not installed.")
