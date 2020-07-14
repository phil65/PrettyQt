# -*- coding: utf-8 -*-

"""gui module

contains QWebEngineView-based classes
"""

try:
    from .winjumplistcategory import WinJumpListCategory
    from .winjumplistitem import WinJumpListItem
    from .winjumplist import WinJumpList

    __all__ = ["WinJumpListCategory", "WinJumpListItem", "WinJumpList"]
except (ImportError, ModuleNotFoundError):
    pass
