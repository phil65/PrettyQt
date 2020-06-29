# -*- coding: utf-8 -*-

"""gui module

contains QWebEngineView-based classes
"""
try:
    from .webengineview import WebEngineView
    __all__ = ["WebEngineView"]
except ModuleNotFoundError:
    pass
