# -*- coding: utf-8 -*-

"""gui module

contains QWebEngineView-based classes
"""

import logging

try:
    from .webengineview import WebEngineView
    __all__ = ["WebEngineView"]
except ModuleNotFoundError:
    logging.warning("Tried to import WebEngineView but not installed.")
