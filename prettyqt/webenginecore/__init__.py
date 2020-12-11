"""Webenginewidgets module.

contains QtWebEngineCore-based classes
"""

import logging

logger = logging.getLogger(__name__)

try:
    from .webenginehttprequest import WebEngineHttpRequest
    from .webengineurlscheme import WebEngineUrlScheme
    from .webengineurlschemehandler import WebEngineUrlSchemeHandler

    __all__ = ["WebEngineHttpRequest", "WebEngineUrlScheme", "WebEngineUrlSchemeHandler"]
except ModuleNotFoundError:
    logger.warning("Tried to import WebEngine module but not installed.")
