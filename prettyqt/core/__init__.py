# -*- coding: utf-8 -*-

"""Core module.

Contains QtCore-based classes
"""

# from qtpy.QtCore import Signal

from qtpy.QtCore import Slot, Signal, Property
from qtpy.QtCore import QModelIndex as ModelIndex
from qtpy.QtCore import QPoint as Point
from qtpy.QtCore import QPointF as PointF
from qtpy.QtCore import QSizeF as SizeF
from qtpy.QtCore import QRect as Rect
from qtpy.QtCore import QRectF as RectF
from qtpy.QtCore import qInstallMessageHandler as install_message_handler
from .persistentmodelindex import PersistentModelIndex
from .uuid import Uuid

# from .debug import Debug
from .line import Line
from .linef import LineF
from .easingcurve import EasingCurve
from .deadlinetimer import DeadlineTimer
from .object import Object
from .margins import Margins
from .marginsf import MarginsF
from .library import Library
from .pluginloader import PluginLoader
from .locale import Locale
from .textstream import TextStream
from .eventloop import EventLoop
from .abstractanimation import AbstractAnimation
from .variantanimation import VariantAnimation
from .propertyanimation import PropertyAnimation
from .animationgroup import AnimationGroup
from .parallelanimationgroup import ParallelAnimationGroup
from .sequentialanimationgroup import SequentialAnimationGroup
from .versionnumber import VersionNumber
from .operatingsystemversion import OperatingSystemVersion
from .libraryinfo import LibraryInfo
from .datastream import DataStream
from .bytearray import ByteArray
from .bytearraymatcher import ByteArrayMatcher
from .url import Url
from .urlquery import UrlQuery
from .coreapplication import CoreApplication
from .iodevice import IODevice
from .filedevice import FileDevice
from .file import File
from .temporaryfile import TemporaryFile
from .buffer import Buffer
from .settings import Settings
from .timezone import TimeZone
from .date import Date
from .time import Time
from .datetime import DateTime

from .size import Size
from .fileinfo import FileInfo

# from .sizef import SizeF
# from .point import Point
# from .pointf import PointF
from .textboundaryfinder import TextBoundaryFinder
from .timer import Timer
from .translator import Translator
from .thread import Thread
from .process import Process

# from .rect import Rect
# from .rectf import RectF
from .regularexpressionmatch import RegularExpressionMatch
from .regularexpressionmatchiterator import RegularExpressionMatchIterator
from .regexp import RegExp
from .regularexpression import RegularExpression
from .mimedata import MimeData
from .runnable import Runnable

# from .modelindex import ModelIndex
from .threadpool import ThreadPool
from .dir import Dir
from .event import Event
from .itemselectionmodel import ItemSelectionModel
from .itemselection import ItemSelection
from .diriterator import DirIterator
from .abstractitemmodel import AbstractItemModel
from .abstractproxymodel import AbstractProxyModel
from .abstractlistmodel import AbstractListModel
from .stringlistmodel import StringListModel
from .sortfilterproxymodel import SortFilterProxyModel
from .abstracttablemodel import AbstractTableModel
from .standardpaths import StandardPaths
from .abstracttransition import AbstractTransition
from .signaltransition import SignalTransition
from .eventtransition import EventTransition
from .abstractstate import AbstractState
from .finalstate import FinalState
from .historystate import HistoryState
from .state import State

if VersionNumber.get_qt_version() >= (5, 13, 0):
    from .concatenatetablesproxymodel import ConcatenateTablesProxyModel
    from .transposeproxymodel import TransposeProxyModel


def app():
    if CoreApplication.instance() is not None:
        return CoreApplication.instance()
    return CoreApplication([])


__all__ = [
    "app",
    "Object",
    "Uuid",
    # "Debug",
    "DeadlineTimer",
    "Margins",
    "MarginsF",
    "Locale",
    "TextStream",
    "EventLoop",
    "DataStream",
    "VersionNumber",
    "OperatingSystemVersion",
    "LibraryInfo",
    "PersistentModelIndex",
    "ByteArray",
    "ByteArrayMatcher",
    "Url",
    "Library",
    "PluginLoader",
    "UrlQuery",
    "CoreApplication",
    "IODevice",
    "FileDevice",
    "File",
    "TemporaryFile",
    "Buffer",
    "Settings",
    "TimeZone",
    "Date",
    "Time",
    "DateTime",
    "Size",
    "SizeF",
    "FileInfo",
    "Point",
    "PointF",
    "Line",
    "LineF",
    "EasingCurve",
    "AbstractAnimation",
    "AnimationGroup",
    "ParallelAnimationGroup",
    "SequentialAnimationGroup",
    "VariantAnimation",
    "PropertyAnimation",
    "TextBoundaryFinder",
    "Timer",
    "Translator",
    "Thread",
    "Process",
    "Rect",
    "RectF",
    "MimeData",
    "Dir",
    "Event",
    "DirIterator",
    "ItemSelectionModel",
    "ItemSelection",
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
    "StringListModel",
    "SortFilterProxyModel",
    "ConcatenateTablesProxyModel",
    "TransposeProxyModel",
    "AbstractTableModel",
    "StandardPaths",
    "AbstractState",
    "FinalState",
    "HistoryState",
    "State",
    "AbstractTransition",
    "SignalTransition",
    "EventTransition",
    "install_message_handler",
]
