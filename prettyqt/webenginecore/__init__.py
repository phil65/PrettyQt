# -*- coding: utf-8 -*-

"""Webenginewidgets module.

contains QtWebEngineCore-based classes
"""

import logging

logger = logging.getLogger(__name__)

try:
    from .webengineurlscheme import WebEngineUrlScheme

    __all__ = ["WebEngineUrlScheme"]
except ModuleNotFoundError:
    logger.warning("Tried to import WebEngine module but not installed.")
