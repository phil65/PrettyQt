from __future__ import annotations

import datetime
import os
import pathlib
from typing import TYPE_CHECKING, Any, Protocol, Union


def make_serializable(obj):
    #  possible to avoid importing by checking the metaobject instead of isinstance?
    from prettyqt import core
    from prettyqt.qt import QtCore

    match obj:
        case QtCore.QMargins():
            return core.Margins(obj)
        case QtCore.QLocale():
            return core.Locale(obj)
        case QtCore.QKeyCombination():
            return core.KeyCombination(obj)
        case QtCore.QUrl():
            return core.Url(obj)
        case QtCore.QEasingCurve():
            return core.EasingCurve(obj)
        case list():
            return [make_serializable(i) for i in obj]

    from prettyqt import gui
    from prettyqt.qt import QtGui

    match obj:
        case QtGui.QPalette():
            return gui.Palette(obj)
        case QtGui.QFont():
            return gui.Font(obj)
        case QtGui.QCursor():
            return gui.Cursor(obj)
        case QtGui.QBrush():
            return gui.Brush(obj)
        case QtGui.QPixmap():
            return gui.Pixmap(obj)
        case QtGui.QRegion():
            return gui.Region(obj)
        case QtGui.QKeySequence():
            return gui.KeySequence(obj)
        case QtGui.QIcon():
            return gui.Icon(obj)
        case QtGui.QVector3D():
            # PyQt doesnt allow Vector3D in ctor
            return gui.Vector3D(obj.x(), obj.y(), obj.z())
        case QtGui.QVector4D():
            # PyQt doesnt allow Vector4D in ctor
            return gui.Vector4D(obj.x(), obj.y(), obj.z(), obj.w())
        case QtGui.QTextDocument():
            # TODO: cant serialize this yet
            return None

    from prettyqt import widgets
    from prettyqt.qt import QtWidgets

    match obj:
        case QtWidgets.QSizePolicy():
            return widgets.SizePolicy.clone(obj)
        case _:
            return obj


if TYPE_CHECKING:
    from prettyqt.qt import QtCore, QtGui, QtWebEngineCore, QtWidgets

    JSONType = Union[str, int, float, bool, None, dict[str, Any], list[Any]]
    PathType = Union[str, os.PathLike]
    UrlType = Union[str, QtCore.QUrl]
    PointType = Union[tuple[int, int], QtCore.QPoint]
    PointFType = Union[tuple[float, float], QtCore.QPointF]
    SizeType = Union[tuple[int, int], QtCore.QSize]
    SizeFType = Union[tuple[float, float], QtCore.QSizeF]
    MarginsType = Union[tuple[int, int, int, int], QtCore.QMargins]
    MarginsFType = Union[tuple[float, float, float, float], QtCore.QMarginsF]
    RectType = Union[tuple[int, int, int, int], QtCore.QRect]
    RectFType = Union[tuple[float, float, float, float], QtCore.QRectF]
    SemanticVersionType = Union[str, QtCore.QVersionNumber, tuple[int, int, int]]
    IconType = Union[QtGui.QIcon, str, pathlib.Path, None]
    ByteArrayType = Union[str, bytes, QtCore.QByteArray]
    TimeType = Union[QtCore.QTime, datetime.time, str]
    DateType = Union[QtCore.QDate, datetime.date, str]
    DateTimeType = Union[QtCore.QDateTime, datetime.datetime, str]
    # ContainerType = Union[widgets.Layout, widgets.Splitter]
    TransformType = Union[
        QtGui.QTransform,
        tuple[float, float, float, float, float, float, float, float, float],
        tuple[float, float, float, float, float, float],
    ]
    VectorType = Union[
        QtGui.QVector3D,
        QtGui.QVector2D,
        QtGui.QVector4D,
        QtCore.QPoint,
        QtCore.QPointF,
        tuple[float, float, float],
    ]
    ColorType = Union[
        str,
        int,
        QtCore.Qt.GlobalColor,
        QtGui.QColor,
        tuple[int, int, int],
        tuple[int, int, int, int],
        None,
    ]
    KeyCombinationType = Union[
        str, QtCore.QKeyCombination, QtCore.QKeySequence, QtGui.QKeySequence.StandardKey
    ]
    ColorAndBrushType = Union[ColorType, QtGui.QBrush]

    VariantType = Union[
        QtCore.QPersistentModelIndex,
        QtCore.QModelIndex,
        QtCore.QJsonDocument,
        # QtCore.QJsonArray,
        # QtCore.QJsonObject,
        QtCore.QJsonValue,
        QtCore.QUrl,
        QtCore.QUuid,
        QtCore.QEasingCurve,
        QtCore.QRegularExpression,
        QtCore.QLocale,
        QtCore.QRectF,
        QtCore.QRect,
        QtCore.QLineF,
        QtCore.QLine,
        QtCore.QPointF,
        QtCore.QPoint,
        QtCore.QSizeF,
        QtCore.QSize,
        QtCore.QDateTime,
        QtCore.QTime,
        QtCore.QDate,
        QtCore.QByteArray,
        QtGui.QColor,
        QtGui.QImage,
        QtGui.QBrush,
        QtGui.QBitmap,
        QtGui.QCursor,
        QtGui.QFont,
        QtGui.QKeySequence,
        QtGui.QIcon,
        QtGui.QTransform,
        QtGui.QPalette,
        QtGui.QMatrix4x4,
        QtGui.QPen,
        QtGui.QPixmap,
        QtGui.QPolygon,
        QtGui.QPolygonF,
        QtGui.QRegion,
        QtWidgets.QSizePolicy,
        QtGui.QTextFormat,
        QtGui.QTextLength,
        QtGui.QVector2D,
        QtGui.QVector3D,
        QtGui.QVector4D,
        bool,
        str,
        int,
        float,
        bytes,
    ]

    Variant = Union[VariantType, list[VariantType], dict[str, VariantType]]

    class Validatable(Protocol):
        """An object with an isValid method (e.g. QUrl)."""

        def isValid(self) -> bool:
            ...

    class SupportsValue(Protocol):
        """An object with a set_value and get_value method."""

        def set_value(self, value):
            ...

        def get_value(self, value):
            ...

    QtSerializableType = Union[
        QtCore.QByteArray,
        QtCore.QUrl,
        QtGui.QBrush,
        QtGui.QColor,
        QtGui.QCursor,
        QtGui.QIcon,
        QtGui.QIconEngine,
        QtGui.QImage,
        QtGui.QPalette,
        QtGui.QPen,
        QtGui.QPicture,
        QtGui.QPixmap,
        QtGui.QPolygon,
        QtGui.QPolygonF,
        QtGui.QRegion,
        QtGui.QStandardItem,
        QtGui.QTransform,
        QtWidgets.QListWidgetItem,
        QtWidgets.QTreeWidgetItem,
        # QtGui.QColorSpace,
        QtWebEngineCore.QWebEngineHistory,
    ]
