"""Core module.

Contains QtCore-based classes
"""

# from qtpy.QtCore import Signal

import qtpy

from qtpy.QtCore import Slot, Signal, Property
from qtpy.QtCore import QModelIndex as ModelIndex
from qtpy.QtCore import QPoint as Point
from qtpy.QtCore import QPointF as PointF
from qtpy.QtCore import QRect as Rect
from qtpy.QtCore import QRectF as RectF
from qtpy.QtCore import qInstallMessageHandler as install_message_handler
from qtpy.QtCore import QEvent as Event
from qtpy.QtCore import QChildEvent as ChildEvent
from qtpy.QtCore import QTimerEvent as TimerEvent
from qtpy.QtCore import QDynamicPropertyChangeEvent as DynamicPropertyChangeEvent
from .persistentmodelindex import PersistentModelIndex
from .cryptographichash import CryptographicHash
from .uuid import Uuid
from .signalblocker import SignalBlocker

# from .debug import Debug
from .line import Line
from .linef import LineF
from .easingcurve import EasingCurve
from .processenvironment import ProcessEnvironment
from .randomgenerator import RandomGenerator

# from .randomgenerator64 import RandomGenerator64
from .deadlinetimer import DeadlineTimer
from .elapsedtimer import ElapsedTimer
from .basictimer import BasicTimer
from .object import Object
from .socketnotifier import SocketNotifier
from .signalmapper import SignalMapper
from .timeline import TimeLine
from .margins import Margins
from .marginsf import MarginsF
from .locale import Locale
from .abstracteventdispatcher import AbstractEventDispatcher
from .textstream import TextStream
from .eventloop import EventLoop
from .abstractanimation import AbstractAnimation
from .variantanimation import VariantAnimation
from .propertyanimation import PropertyAnimation
from .pauseanimation import PauseAnimation
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
from .translator import Translator
from .coreapplication import CoreApplication
from .filesystemwatcher import FileSystemWatcher
from .iodevice import IODevice
from .filedevice import FileDevice
from .file import File
from .savefile import SaveFile
from .lockfile import LockFile
from .buffer import Buffer
from .settings import Settings
from .timezone import TimeZone
from .date import Date
from .time import Time
from .datetime import DateTime
from .calendar import Calendar
from .resource import Resource
from .size import Size
from .sizef import SizeF
from .fileinfo import FileInfo
from .storageinfo import StorageInfo

# from .point import Point
# from .pointf import PointF
from .textboundaryfinder import TextBoundaryFinder
from .timer import Timer
from .thread import Thread
from .process import Process

# from .rect import Rect
# from .rectf import RectF
from .regularexpressionmatch import RegularExpressionMatch
from .regularexpressionmatchiterator import RegularExpressionMatchIterator
from .regexp import RegExp
from .regularexpression import RegularExpression
from .mimetype import MimeType
from .mimedata import MimeData
from .mimedatabase import MimeDatabase
from .runnable import Runnable

# from .modelindex import ModelIndex
from .threadpool import ThreadPool
from .dir import Dir
from .temporaryfile import TemporaryFile
from .temporarydir import TemporaryDir

# from .event import Event
from .itemselectionmodel import ItemSelectionModel
from .itemselection import ItemSelection
from .itemselectionrange import ItemSelectionRange
from .diriterator import DirIterator
from .abstractitemmodel import AbstractItemModel
from .abstractproxymodel import AbstractProxyModel
from .identityproxymodel import IdentityProxyModel
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
from .statemachine import StateMachine
from .commandlineoption import CommandLineOption
from .commandlineparser import CommandLineParser
from .collatorsortkey import CollatorSortKey
from .collator import Collator

from .jsonvalue import JsonValue
from .jsondocument import JsonDocument

# not available in PySide2
if qtpy.API == "pyqt5":
    from .library import Library
    from .pluginloader import PluginLoader

if VersionNumber.get_qt_version() >= (5, 13, 0):
    from .concatenatetablesproxymodel import ConcatenateTablesProxyModel
    from .transposeproxymodel import TransposeProxyModel


def app():
    if CoreApplication.instance() is not None:
        return CoreApplication.instance()
    return CoreApplication([])


__all__ = [
    "app",
    "Event",
    "ChildEvent",
    "TimerEvent",
    "DynamicPropertyChangeEvent",
    "Object",
    "CryptographicHash",
    "Uuid",
    "SignalBlocker",
    "SignalMapper",
    "SocketNotifier",
    # "Debug",
    "DeadlineTimer",
    "ElapsedTimer",
    "BasicTimer",
    "Margins",
    "MarginsF",
    "Locale",
    "AbstractEventDispatcher",
    "Resource",
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
    "FileSystemWatcher",
    "IODevice",
    "FileDevice",
    "File",
    "SaveFile",
    "LockFile",
    "TemporaryFile",
    "Buffer",
    "Settings",
    "TimeZone",
    "Date",
    "Time",
    "DateTime",
    "Calendar",
    "Size",
    "SizeF",
    "FileInfo",
    "StorageInfo",
    "Point",
    "PointF",
    "Line",
    "LineF",
    "EasingCurve",
    "ProcessEnvironment",
    "TimeLine",
    "RandomGenerator",
    # "RandomGenerator64",
    "AbstractAnimation",
    "AnimationGroup",
    "ParallelAnimationGroup",
    "SequentialAnimationGroup",
    "VariantAnimation",
    "PropertyAnimation",
    "PauseAnimation",
    "TextBoundaryFinder",
    "Timer",
    "Translator",
    "Thread",
    "Process",
    "Rect",
    "RectF",
    "MimeType",
    "MimeData",
    "MimeDatabase",
    "Dir",
    "TemporaryDir",
    "DirIterator",
    "ItemSelectionModel",
    "ItemSelection",
    "ItemSelectionRange",
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
    "IdentityProxyModel",
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
    "StateMachine",
    "AbstractTransition",
    "SignalTransition",
    "EventTransition",
    "CommandLineOption",
    "CommandLineParser",
    "install_message_handler",
    "CollatorSortKey",
    "Collator",
    "JsonValue",
    "JsonDocument",
]
