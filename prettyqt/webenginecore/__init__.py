"""Webenginewidgets module.

contains QtWebEngineCore-based classes
"""

import logging

logger = logging.getLogger(__name__)

try:
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

    __all__ = [
        "WebEngineHttpRequest",
        "WebEngineUrlScheme",
        "WebEngineHistoryItem",
        "WebEngineContextMenuRequest",
        "WebEngineDownloadRequest",
        "WebEngineHistory",
        "WebEngineUrlSchemeHandler",
        "WebEngineSettings",
        "WebEngineScript",
        "WebEngineScriptCollection",
        "WebEngineProfile",
        "WebEnginePage",
    ]
except ModuleNotFoundError:
    logger.warning("Tried to import WebEngine module but not installed.")
