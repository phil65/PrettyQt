# -*- coding: utf-8 -*-

"""Webenginewidgets module.

contains QtWebEngineCore-based classes
"""

import logging

logger = logging.getLogger(__name__)

try:
    from .webengineurlscheme import WebEngineUrlScheme
    from .webengineurlschemehandler import WebEngineUrlSchemeHandler

    __all__ = ["WebEngineUrlScheme", "WebEngineUrlSchemeHandler"]
except ModuleNotFoundError:
    logger.warning("Tried to import WebEngine module but not installed.")
