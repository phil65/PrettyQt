# -*- coding: utf-8 -*-

"""Webenginewidgets module.

contains QWebEngineView-based classes
"""

import logging

logger = logging.getLogger(__name__)

try:
    from .webengineview import WebEngineView
    from .webenginepage import WebEnginePage
    from .webengineprofile import WebEngineProfile

    __all__ = ["WebEngineView", "WebEnginePage", "WebEngineProfile"]
except ModuleNotFoundError:
    logger.warning("Tried to import WebEngineView but not installed.")
