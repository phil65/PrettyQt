# -*- coding: utf-8 -*-

"""gui module

contains QWebEngineView-based classes
"""

import logging

try:
    from .webengineview import WebEngineView
    from .webenginepage import WebEnginePage

    __all__ = ["WebEngineView", "WebEnginePage"]
except ModuleNotFoundError:
    logging.warning("Tried to import WebEngineView but not installed.")
