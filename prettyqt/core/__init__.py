"""Core non-graphical classes used by other modules."""

from __future__ import annotations

import contextlib
import sys
from prettyqt.qt import QtCore


from prettyqt.qt.QtCore import *  # noqa: F403

from prettyqt.qt.QtCore import (
    qInstallMessageHandler as install_message_handler,
    QtMsgType as MsgType,
    Signal,
    # Property,
    QEnum as Enum,
    QPoint as Point,
    QPointF as PointF,
    QModelIndex as ModelIndex,
    QRect as Rect,
    QRectF as RectF,
    # QtCriticalMsg as CriticalMsg,
    # QtDebugMsg as DebugMsg,
    # QtFatalMsg as FatalMsg,
    # QtInfoMsg as InfoMsg,
    # QtSystemMsg as SystemMsg,
    # QtWarningMsg as WarningMsg,
)

from .event import Event
from .slot import Slot

from .property import Property
from .loggingcategory import LoggingCategory
from .timezone import TimeZone
from .date import Date
from ._time import Time
from ._datetime import DateTime
from .semaphore import Semaphore
from .mutex import Mutex
from .metaenum import MetaEnum
from .metamethod import MetaMethod
from .metaproperty import MetaProperty
from .metatype import MetaType
from .metaobject import MetaObject
from .modelroledata import ModelRoleData
from .persistentmodelindex import PersistentModelIndex
from .cryptographichash import CryptographicHash
from .uuid import Uuid, UuidMixin
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
from .object import Object, ObjectMixin
from .socketnotifier import SocketNotifier
from .sharedmemory import SharedMemory
from .signalmapper import SignalMapper
from .timeline import TimeLine
from .margins import Margins
from .marginsf import MarginsF
from ._locale import Locale
from .abstracteventdispatcher import AbstractEventDispatcher
from .textstream import TextStream
from .eventloop import EventLoop
from .abstractanimation import AbstractAnimation, AbstractAnimationMixin
from .variantanimation import VariantAnimation, VariantAnimationMixin
from .propertyanimation import PropertyAnimation
from .pauseanimation import PauseAnimation
from .animationgroup import AnimationGroup, AnimationGroupMixin
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
from .coreapplication import CoreApplication, CoreApplicationMixin
from .filesystemwatcher import FileSystemWatcher
from .fileselector import FileSelector
from .iodevice import IODevice, IODeviceMixin
from .filedevice import FileDevice, FileDeviceMixin
from .file import File, FileMixin
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
from .mimedatabase import MimeDatabase
from .mimedata import MimeData
from .runnable import Runnable

# from .modelindex import ModelIndex
from .threadpool import ThreadPool
from .dir import Dir
from .temporaryfile import TemporaryFile
from .temporarydir import TemporaryDir
from .keycombination import KeyCombination

# from .event import Event
from .itemselectionmodel import ItemSelectionModel
from .itemselection import ItemSelection
from .itemselectionrange import ItemSelectionRange
from .diriterator import DirIterator
from .abstractitemmodel import AbstractItemModel, AbstractItemModelMixin
from .abstractproxymodel import AbstractProxyModel, AbstractProxyModelMixin
from .identityproxymodel import IdentityProxyModel
from .abstractlistmodel import AbstractListModel, AbstractListModelMixin
from .stringlistmodel import StringListModel, StringListModelMixin
from .sortfilterproxymodel import SortFilterProxyModel
from .abstracttablemodel import AbstractTableModel, AbstractTableModelMixin
from .standardpaths import StandardPaths
from .xmlstreamreader import XmlStreamReader
from .commandlineoption import CommandLineOption
from .commandlineparser import CommandLineParser
from .collatorsortkey import CollatorSortKey
from .collator import Collator

from .jsonvalue import JsonValue
from .jsondocument import JsonDocument

from .library import Library  # type: ignore
from .pluginloader import PluginLoader  # type: ignore

from .concatenatetablesproxymodel import ConcatenateTablesProxyModel
from .transposeproxymodel import TransposeProxyModel
from prettyqt.qt import QtCore

QT_MODULE = QtCore


@contextlib.contextmanager
def update_property_group():
    QtCore.Qt.beginPropertyUpdateGroup()
    yield None
    QtCore.Qt.endPropertyUpdateGroup()


def app(args: list[str] | None = None, **kwargs) -> CoreApplication:
    if (instance := CoreApplication.instance()) is not None:
        return instance
    return CoreApplication(sys.argv if args is None else args, **kwargs)


__all__ = [
    "app",
    "Event",
    # "ChildEvent",
    # "TimerEvent",
    "Enum",
    # "ClassInfo",
    # "Q_ARG",
    # "Q_RETURN_ARG",
    # "DynamicPropertyChangeEvent",
    "MetaEnum",
    "LoggingCategory",
    "PersistentModelIndex",
    "MetaMethod",
    "MetaProperty",
    "MetaType",
    "MetaObject",
    "Object",
    "ObjectMixin",
    "CryptographicHash",
    "Uuid",
    "UuidMixin",
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
    "ModelRoleData",
    "PersistentModelIndex",
    "ByteArray",
    "ByteArrayMatcher",
    "Url",
    "Library",
    "PluginLoader",
    "UrlQuery",
    "CoreApplication",
    "CoreApplicationMixin",
    "FileSystemWatcher",
    "FileSelector",
    "IODevice",
    "IODeviceMixin",
    "FileDevice",
    "FileDeviceMixin",
    "File",
    "FileMixin",
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
    "AbstractAnimationMixin",
    "AnimationGroup",
    "AnimationGroupMixin",
    "ParallelAnimationGroup",
    "SequentialAnimationGroup",
    "VariantAnimation",
    "VariantAnimationMixin",
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
    "KeyCombination",
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
    # "SignalInstance",
    "AbstractItemModel",
    "AbstractItemModelMixin",
    "AbstractProxyModel",
    "AbstractProxyModelMixin",
    "IdentityProxyModel",
    "AbstractListModel",
    "AbstractListModelMixin",
    "StringListModel",
    "StringListModelMixin",
    "SortFilterProxyModel",
    "ConcatenateTablesProxyModel",
    "TransposeProxyModel",
    "AbstractTableModel",
    "AbstractTableModelMixin",
    "StandardPaths",
    "XmlStreamReader",
    # "AbstractState",
    # "FinalState",
    # "HistoryState",
    # "State",
    # "StateMachine",
    # "AbstractTransition",
    # "SignalTransition",
    # "EventTransition",
    "CommandLineOption",
    "CommandLineParser",
    "install_message_handler",
    "CollatorSortKey",
    "Collator",
    "JsonValue",
    "JsonDocument",
    "MsgType",
    # "CriticalMsg",
    # "DebugMsg",
    # "FatalMsg",
    # "InfoMsg",
    # "SystemMsg",
    # "WarningMsg",
    "Semaphore",
    "Mutex",
    "SharedMemory",
]
