# -*- coding: utf-8 -*-

"""core module

contains QtCore-based classes
"""

# from qtpy.QtCore import Signal

from .settings import Settings
from .size import Size
from .rect import Rect
from .filesystemmodel import FileSystemModel

__all__ = ["Settings", "Size", "Rect", "FileSystemModel"]
