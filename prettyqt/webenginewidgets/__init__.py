# -*- coding: utf-8 -*-

"""Webenginewidgets module.

contains QtWebEngineWidgets-based classes
"""

import logging

logger = logging.getLogger(__name__)

try:
    from .webenginehistoryitem import WebEngineHistoryItem
    from .webenginehistory import WebEngineHistory
    from .webenginesettings import WebEngineSettings
    from .webenginescript import WebEngineScript
    from .webenginescriptcollection import WebEngineScriptCollection
    from .webengineview import WebEngineView
    from .webenginepage import WebEnginePage
    from .webengineprofile import WebEngineProfile
    from .webenginedownloaditem import WebEngineDownloadItem

    __all__ = [
        "WebEngineHistoryItem",
        "WebEngineSettings",
        "WebEngineHistory",
        "WebEngineView",
        "WebEnginePage",
        "WebEngineProfile",
        "WebEngineDownloadItem",
        "WebEngineScript",
        "WebEngineScriptCollection",
    ]
except ModuleNotFoundError:
    logger.warning("Tried to import WebEngine module but not installed.")
