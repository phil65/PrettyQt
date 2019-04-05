# -*- coding: utf-8 -*-

"""core module

contains QtCore-based classes
"""

# from qtpy.QtCore import Signal

from .settings import Settings
from .size import Size
from .rect import Rect

__all__ = ["Settings", "Size", "Rect"]
