# -*- coding: utf-8 -*-

"""Webenginewidgets module.

contains QtWebEngineWidgets-based classes
"""

import logging

logger = logging.getLogger(__name__)

try:
    from .webenginehistoryitem import WebEngineHistoryItem
    from .webenginehistory import WebEngineHistory
    from .webengineview import WebEngineView
    from .webenginepage import WebEnginePage
    from .webengineprofile import WebEngineProfile
    from .webenginedownloaditem import WebEngineDownloadItem
    from .webenginescript import WebEngineScript

    __all__ = [
        "WebEngineHistoryItem",
        "WebEngineHistory",
        "WebEngineView",
        "WebEnginePage",
        "WebEngineProfile",
        "WebEngineDownloadItem",
        "WebEngineScript",
    ]
except ModuleNotFoundError:
    logger.warning("Tried to import WebEngine module but not installed.")
