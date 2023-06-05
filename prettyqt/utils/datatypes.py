from __future__ import annotations

from abc import ABCMeta
import datetime
import os
import pathlib
from typing import TYPE_CHECKING, Any, Protocol
from re import Pattern

from prettyqt.qt import QtCore


class QABCMeta(type(QtCore.QObject), ABCMeta):
    pass


def make_qtype(obj):
    from prettyqt import core

    match obj:
        case core.Margins():
            return QtCore.QMargins(obj)
        case core.Locale():
            return QtCore.QLocale(obj)
        case core.KeyCombination():
            return QtCore.QKeyCombination(obj)
        case core.Url():
            return QtCore.QUrl(obj)
        case core.EasingCurve():
            return QtCore.QEasingCurve(obj)
        case list():
            return [make_qtype(i) for i in obj]

    from prettyqt import gui
    from prettyqt.qt import QtGui

    match obj:
        case gui.Palette():
            return QtGui.QPalette(obj)
        case gui.Font():
            return QtGui.QFont(obj)
        case gui.Color():
            return obj.convertTo(obj.spec())
        case gui.Cursor():
            return QtGui.QCursor(obj)
        case gui.Brush():
            return QtGui.QBrush(obj)
        case gui.Pixmap():
            return QtGui.QPixmap(obj)
        case gui.Region():
            return QtGui.QRegion(obj)
        case gui.KeySequence():
            return QtGui.QKeySequence(obj)
        case gui.Icon():
            return QtGui.QIcon(obj)
        case gui.Vector3D():
            # PyQt doesnt allow Vector3D in ctor
            return QtGui.QVector3D(obj.x(), obj.y(), obj.z())
        case gui.Vector4D():
            # PyQt doesnt allow Vector4D in ctor
            return QtGui.QVector4D(obj.x(), obj.y(), obj.z(), obj.w())
    return obj


def make_serializable(obj):
    #  possible to avoid importing by checking the metaobject instead of isinstance?
    from prettyqt import core

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
    from prettyqt.qt import QtGui, QtWidgets

    JSONType = str | int | float | bool | None | dict[str, Any] | list[Any]
    PathType = str | os.PathLike
    PatternType = str | Pattern
    UrlType = str | QtCore.QUrl
    PointType = tuple[int, int] | QtCore.QPoint
    PointFType = tuple[float, float] | QtCore.QPointF
    SizeType = tuple[int, int] | QtCore.QSize
    SizeFType = tuple[float, float] | QtCore.QSizeF
    MarginsType = tuple[int, int, int, int] | QtCore.QMargins
    MarginsFType = tuple[float, float, float, float] | QtCore.QMarginsF
    RectType = tuple[int, int, int, int] | QtCore.QRect
    RectFType = tuple[float, float, float, float] | QtCore.QRectF
    SemanticVersionType = str | QtCore.QVersionNumber | tuple[int, int, int]
    IconType = QtGui.QIcon | str | pathlib.Path | None
    ByteArrayType = str | bytes | QtCore.QByteArray
    TimeType = QtCore.QTime | datetime.time | str
    DateType = QtCore.QDate | datetime.date | str
    DateTimeType = QtCore.QDateTime | datetime.datetime | str
    # ContainerType = Union[widgets.Layout, widgets.Splitter]
    TransformType = (
        QtGui.QTransform
        | tuple[float, float, float, float, float, float, float, float, float]
        | tuple[float, float, float, float, float, float]
    )
    VectorType = (
        QtGui.QVector3D
        | QtGui.QVector2D
        | QtGui.QVector4D
        | QtCore.QPoint
        | QtCore.QPointF
        | tuple[float, float, float]
    )
    ColorType = (
        str
        | int
        | QtCore.Qt.GlobalColor
        | QtGui.QColor
        | tuple[int, int, int]
        | tuple[int, int, int, int]
        | None
    )
    KeyCombinationType = (
        str | QtCore.QKeyCombination | QtGui.QKeySequence | QtGui.QKeySequence.StandardKey
    )
    ColorAndBrushType = ColorType | QtGui.QBrush

    VariantType = (
        QtCore.QPersistentModelIndex
        | QtCore.QModelIndex
        | QtCore.QJsonDocument
        |
        # QtCore.QJsonArray |
        # QtCore.QJsonObject |
        QtCore.QJsonValue
        | QtCore.QUrl
        | QtCore.QUuid
        | QtCore.QEasingCurve
        | QtCore.QRegularExpression
        | QtCore.QLocale
        | QtCore.QRectF
        | QtCore.QRect
        | QtCore.QLineF
        | QtCore.QLine
        | QtCore.QPointF
        | QtCore.QPoint
        | QtCore.QSizeF
        | QtCore.QSize
        | QtCore.QDateTime
        | QtCore.QTime
        | QtCore.QDate
        | QtCore.QByteArray
        | QtGui.QColor
        | QtGui.QImage
        | QtGui.QBrush
        | QtGui.QBitmap
        | QtGui.QCursor
        | QtGui.QFont
        | QtGui.QKeySequence
        | QtGui.QIcon
        | QtGui.QTransform
        | QtGui.QPalette
        | QtGui.QMatrix4x4
        | QtGui.QPen
        | QtGui.QPixmap
        | QtGui.QPolygon
        | QtGui.QPolygonF
        | QtGui.QRegion
        | QtWidgets.QSizePolicy
        | QtGui.QTextFormat
        | QtGui.QTextLength
        | QtGui.QVector2D
        | QtGui.QVector3D
        | QtGui.QVector4D
        | bool
        | str
        | int
        | float
        | bytes
    )

    Variant = VariantType | list[VariantType] | dict[str, VariantType]

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

    QtSerializableType = (
        QtCore.QByteArray
        | QtCore.QUrl
        | QtGui.QBrush
        | QtGui.QColor
        | QtGui.QCursor
        | QtGui.QIcon
        | QtGui.QIconEngine
        | QtGui.QImage
        | QtGui.QPalette
        | QtGui.QPen
        | QtGui.QPicture
        | QtGui.QPixmap
        | QtGui.QPolygon
        | QtGui.QPolygonF
        | QtGui.QRegion
        | QtGui.QStandardItem
        | QtGui.QTransform
        | QtWidgets.QListWidgetItem
        | QtWidgets.QTreeWidgetItem
    )
    # QtGui.QColorSpace |
    # QtWebEngineCore.QWebEngineHistory
