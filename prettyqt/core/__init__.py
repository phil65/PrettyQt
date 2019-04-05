# -*- coding: utf-8 -*-

"""core module

contains QtCore-based classes
"""

# from qtpy.QtCore import Signal

from .object import Object
from .settings import Settings
from .size import Size
from .rect import Rect
from .mimedata import MimeData
from .runnable import Runnable
from .modelindex import ModelIndex
from .threadpool import ThreadPool
from .filesystemmodel import FileSystemModel

from qtpy.QtCore import Slot, Signal

__all__ = ["Object",
           "Settings",
           "Size",
           "Rect",
           "MimeData",
           "FileSystemModel",
           "Slot",
           "Runnable",
           "ModelIndex",
           "ThreadPool",
           "Signal"]
