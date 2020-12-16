"""winextras module.

contains QtWinExtras-based classes
"""

try:
    from .winjumplistcategory import WinJumpListCategory
    from .winjumplistitem import WinJumpListItem
    from .winjumplist import WinJumpList
    from .winthumbnailtoolbutton import WinThumbnailToolButton

    __all__ = [
        "WinJumpListCategory",
        "WinJumpListItem",
        "WinJumpList",
        "WinThumbnailToolButton",
    ]
except (ImportError, ModuleNotFoundError):
    pass
