# -*- coding: utf-8 -*-

"""gui module

contains QtGui-based classes
"""
try:
    from .webengineview import WebEngineView
    __all__ = ["WebEngineView"]
except ModuleNotFoundError:
    pass
