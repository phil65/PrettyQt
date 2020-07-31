# -*- coding: utf-8 -*-

"""winextras module.

contains QtWinExtras-based classes
"""

try:
    from .winjumplistcategory import WinJumpListCategory
    from .winjumplistitem import WinJumpListItem
    from .winjumplist import WinJumpList

    __all__ = ["WinJumpListCategory", "WinJumpListItem", "WinJumpList"]
except (ImportError, ModuleNotFoundError):
    pass
