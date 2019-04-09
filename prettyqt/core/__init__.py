# -*- coding: utf-8 -*-

"""core module

contains QtCore-based classes
"""

# from qtpy.QtCore import Signal

from .object import Object
from .settings import Settings
from .size import Size
from .point import Point
from .timer import Timer
from .translator import Translator
from .rect import Rect
from .rectf import RectF
from .regexp import RegExp
from .mimedata import MimeData
from .runnable import Runnable
from .modelindex import ModelIndex
from .threadpool import ThreadPool
from .filesystemmodel import FileSystemModel

from qtpy.QtCore import Slot, Signal, Property

__all__ = ["Object",
           "Settings",
           "Size",
           "Point",
           "Timer",
           "Translator",
           "Rect",
           "RectF",
           "MimeData",
           "FileSystemModel",
           "Slot",
           "Property",
           "RegExp",
           "Runnable",
           "ModelIndex",
           "ThreadPool",
           "Signal"]
