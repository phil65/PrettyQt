"""Webenginewidgets module.

contains QtWebEngineCore-based classes
"""

import logging

logger = logging.getLogger(__name__)

try:
    from .webchannel import WebChannel

    __all__ = ["WebChannel"]
except ModuleNotFoundError:
    logger.warning("Tried to import WebEngine module but not installed.")
