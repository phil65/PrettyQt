"""Core module.

Contains QtCore-based classes
"""

# from prettyqt.qt.QtCore import Signal

from __future__ import annotations

import prettyqt.qt

from prettyqt.qt.QtCore import (  # type: ignore
    Slot,
    Signal,
    Property,
    QModelIndex as ModelIndex,
    QPoint as Point,
    QPointF as PointF,
    QRect as Rect,
    QRectF as RectF,
    qInstallMessageHandler as install_message_handler,
    QEvent as Event,
    QChildEvent as ChildEvent,
    QTimerEvent as TimerEvent,
    QDynamicPropertyChangeEvent as DynamicPropertyChangeEvent,
    # QtCriticalMsg as CriticalMsg,
    # QtDebugMsg as DebugMsg,
    # QtFatalMsg as FatalMsg,
    # QtInfoMsg as InfoMsg,
    # QtMsgType as MsgType,
    # QtSystemMsg as SystemMsg,
    # QtWarningMsg as WarningMsg,
)
from .timezone import TimeZone
from .date import Date
from ._time import Time
from ._datetime import DateTime
from .semaphore import Semaphore
from .mutex import Mutex
from .metaenum import MetaEnum
from .metamethod import MetaMethod
from .metaproperty import MetaProperty
from .metaobject import MetaObject
from .persistentmodelindex import PersistentModelIndex
from .cryptographichash import CryptographicHash
from .uuid import Uuid
from .signalblocker import SignalBlocker
from .abstractnativeeventfilter import AbstractNativeEventFilter

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
from .fileselector import FileSelector
from .iodevice import IODevice
from .filedevice import FileDevice
from .file import File
from .savefile import SaveFile
from .lockfile import LockFile
from .buffer import Buffer
from .settings import Settings
from ._calendar import Calendar
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
from .xmlstreamreader import XmlStreamReader
from .commandlineoption import CommandLineOption
from .commandlineparser import CommandLineParser
from .collatorsortkey import CollatorSortKey
from .collator import Collator

from .jsonvalue import JsonValue
from .jsondocument import JsonDocument

# not available in PySide2
if prettyqt.qt.API.startswith("pyqt"):
    from .library import Library  # type: ignore
    from .pluginloader import PluginLoader  # type: ignore

if VersionNumber.get_qt_version() >= (5, 13, 0):
    from .concatenatetablesproxymodel import ConcatenateTablesProxyModel
    from .transposeproxymodel import TransposeProxyModel

# if VersionNumber.get_qt_version() < (6, 0, 0):
#     from .abstracttransition import AbstractTransition
#     from .signaltransition import SignalTransition
#     from .eventtransition import EventTransition
#     from .abstractstate import AbstractState
#     from .finalstate import FinalState
#     from .historystate import HistoryState
#     from .state import State
#     from .statemachine import StateMachine


def app(args: list[str] | None = None) -> CoreApplication:
    instance = CoreApplication.instance()
    if instance is not None:
        return instance
    return CoreApplication([] if args is None else args)


__all__ = [
    "app",
    "Event",
    "ChildEvent",
    "TimerEvent",
    "DynamicPropertyChangeEvent",
    "MetaEnum",
    "MetaMethod",
    "MetaProperty",
    "MetaObject",
    "Object",
    "CryptographicHash",
    "Uuid",
    "SignalBlocker",
    "AbstractNativeEventFilter",
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
    "FileSelector",
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
    "XmlStreamReader",
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
    "CriticalMsg",
    "DebugMsg",
    "FatalMsg",
    "InfoMsg",
    "MsgType",
    "SystemMsg",
    "WarningMsg",
    "Semaphore",
    "Mutex",
]
