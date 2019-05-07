# -*- coding: utf-8 -*-

"""core module

contains QtCore-based classes
"""

# from qtpy.QtCore import Signal

from .object import Object
from .settings import Settings
from .date import Date
from .datetime import DateTime
# from .size import Size
# from .sizef import SizeF
# from .point import Point
# from .pointf import PointF
from .timer import Timer
from .translator import Translator
from .thread import Thread
# from .rect import Rect
# from .rectf import RectF
from .regexp import RegExp
from .mimedata import MimeData
from .runnable import Runnable
from .modelindex import ModelIndex
from .threadpool import ThreadPool
from .dir import Dir
from .diriterator import DirIterator
from .abstractitemmodel import AbstractItemModel
from .sortfilterproxymodel import SortFilterProxyModel
from .abstracttablemodel import AbstractTableModel

from qtpy.QtCore import Slot, Signal, Property
from qtpy.QtCore import QPoint as Point
from qtpy.QtCore import QPointF as PointF
from qtpy.QtCore import QSize as Size
from qtpy.QtCore import QSizeF as SizeF
from qtpy.QtCore import QRect as Rect
from qtpy.QtCore import QRectF as RectF

__all__ = ["Object",
           "Settings",
           "Date",
           "DateTime",
           "Size",
           "SizeF",
           "Point",
           "PointF",
           "Timer",
           "Translator",
           "Thread",
           "Rect",
           "RectF",
           "MimeData",
           "Dir",
           "DirIterator",
           "Slot",
           "Property",
           "RegExp",
           "Runnable",
           "ModelIndex",
           "ThreadPool",
           "Signal",
           "AbstractItemModel",
           "SortFilterProxyModel",
           "AbstractTableModel"]
