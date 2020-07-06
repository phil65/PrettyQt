# -*- coding: utf-8 -*-

"""core module

contains QtCore-based classes
"""

# from qtpy.QtCore import Signal

from .object import Object
from .url import Url
from .coreapplication import CoreApplication
from .iodevice import IODevice
from .filedevice import FileDevice
from .file import File
from .buffer import Buffer
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
from .regularexpressionmatch import RegularExpressionMatch
from .regularexpressionmatchiterator import RegularExpressionMatchIterator
from .regexp import RegExp
from .regularexpression import RegularExpression
from .mimedata import MimeData
from .runnable import Runnable
from .modelindex import ModelIndex
from .threadpool import ThreadPool
from .dir import Dir
from .event import Event
from .itemselectionmodel import ItemSelectionModel
from .diriterator import DirIterator
from .abstractitemmodel import AbstractItemModel
from .abstractproxymodel import AbstractProxyModel
from .abstractlistmodel import AbstractListModel
from .sortfilterproxymodel import SortFilterProxyModel
from .abstracttablemodel import AbstractTableModel

from qtpy.QtCore import Slot, Signal, Property
from qtpy.QtCore import QPoint as Point
from qtpy.QtCore import QPointF as PointF
from qtpy.QtCore import QSize as Size
from qtpy.QtCore import QSizeF as SizeF
from qtpy.QtCore import QRect as Rect
from qtpy.QtCore import QRectF as RectF

__all__ = [
    "Object",
    "Url",
    "CoreApplication",
    "IODevice",
    "FileDevice",
    "File",
    "Buffer",
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
    "Event",
    "DirIterator",
    "ItemSelectionModel",
    "Slot",
    "Property",
    "RegularExpressionMatch",
    "RegularExpressionMatchIterator",
    "RegExp",
    "RegularExpression",
    "Runnable",
    "ModelIndex",
    "ThreadPool",
    "Signal",
    "AbstractItemModel",
    "AbstractProxyModel",
    "AbstractListModel",
    "SortFilterProxyModel",
    "AbstractTableModel",
]
