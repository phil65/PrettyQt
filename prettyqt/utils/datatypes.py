from __future__ import annotations

from abc import ABCMeta
import datetime
import enum
import os
import pathlib
import re
from typing import TYPE_CHECKING, Any, ClassVar, Protocol, runtime_checkable


from prettyqt.qt import QtCore


class QABCMeta(type(QtCore.QObject), ABCMeta):
    pass


def to_string(val: Any, locale: QtCore.QLocale | None = None) -> str:
    from prettyqt import constants, core, gui, widgets

    if locale is None:
        locale = core.Locale()
    match val:
        case str():
            return val
        case bool():
            return "✓" if val else "☐"
        case enum.Flag():
            return val.name
        case enum.Enum():
            return val.name
        case int() | float() | core.QByteArray():
            return locale.toString(val)
        case gui.QColor():
            return f"({val.red()},{val.green()},{val.blue()},{val.alpha()})"
        case gui.QFont():
            return val.family()
        case gui.QRegion():
            rect = val.boundingRect()
            return f"({rect.x()},{rect.y()},{rect.width()},{rect.height()})"
        case gui.QCursor():
            return constants.CURSOR_SHAPE.inverse[val.shape()]
        case gui.QKeySequence():
            return val.toString()
        case core.QDate() | core.QDateTime() | core.QTime():
            return val.toString(constants.DateFormat.ISODate)
        case core.QPoint():
            return f"({val.x()},{val.y()})"
        case core.QRect():
            return f"({val.x()},{val.y()},{val.width()},{val.height()})"
        case core.QSize():
            return f"({val.width()},{val.height()})"
        case core.QLocale():
            return val.bcp47Name()
        case widgets.QSizePolicy():
            return (
                f"({widgets.sizepolicy.SIZE_POLICY.inverse[val.horizontalPolicy()]}, "
                f"{widgets.sizepolicy.SIZE_POLICY.inverse[val.verticalPolicy()]}, "
                f"{widgets.sizepolicy.CONTROL_TYPE.inverse[val.controlType()]})"
            )
        case list():
            return ",".join(map(repr, val))
        case re.Pattern():
            return val.pattern
        case datetime.date():
            return val.isoformat()
        case datetime.datetime():
            return val.isoformat(sep=" ")
        case core.QRegularExpression():
            return val.pattern()
        case core.QUrl():
            return val.toString()
    try:
        import numpy as np
    except ImportError:
        pass
    else:
        match val:
            case np.integer():
                return to_string(int(val), locale)
            case np.floating():
                return to_string(float(val), locale)
            case np.str_():
                return val.astype(str)
            case np.bool_():
                return bool(val.astype(bool))
            case np.datetime64():
                return to_string(val.astype(datetime.datetime), locale)
    return repr(val)


def get_widget_for_value(val, parent=None):
    from prettyqt import core, gui, widgets, custom_widgets

    match val:
        case bool():
            return widgets.CheckBox(parent=parent)
        case enum.Flag():
            widget = custom_widgets.EnumFlagWidget(parent=parent)
            widget._set_enum_class(type(val))
            return widget
        case enum.Enum():
            widget = custom_widgets.EnumComboBox(parent=parent)
            widget._set_enum_class(type(val))
            return widget
        case int():
            return widgets.SpinBox(parent=parent)
        case float():
            return widgets.DoubleSpinBox(parent=parent)
        case pathlib.Path():
            return custom_widgets.FileChooserButton(parent=parent)
        case str():
            widget = widgets.LineEdit(parent=parent)
            widget.setFrame(False)
            return widget
        case core.QRegularExpression() | re.Pattern():
            return custom_widgets.RegexInput(show_error=False, parent=parent)
        case core.QTime():
            return widgets.TimeEdit(parent=parent)
        case core.QDate():
            return widgets.DateEdit(parent=parent)
        case core.QDateTime():
            return widgets.DateTimeEdit(parent=parent)
        case core.QPoint():
            return custom_widgets.PointEdit(parent=parent)
        case core.QSize():
            return custom_widgets.SizeEdit(parent=parent)
        case core.QRect():
            return custom_widgets.RectEdit(parent=parent)
        case gui.QKeySequence():
            return widgets.KeySequenceEdit(parent=parent)
        case gui.QRegion():
            return custom_widgets.RegionEdit(parent=parent)
        case gui.QFont():
            return widgets.FontComboBox(parent=parent)
        case gui.QColor():
            return custom_widgets.ColorComboBox(parent=parent)
        case widgets.QSizePolicy():
            return custom_widgets.SizePolicyEdit(parent=parent)
        case core.QUrl():
            return custom_widgets.UrlLineEdit(parent=parent)
        # case QtCore.QRectF():  # todo
        #     return custom_widgets.RectEdit(parent=parent)
    try:
        import numpy as np
    except ImportError:
        pass
    else:
        match val:
            case np.floating():
                return custom_widgets.FloatLineEdit()
            case np.integer():
                return custom_widgets.IntLineEdit()
            case np.str_():
                return widgets.LineEdit()
            case np.datetime64():
                return widgets.DateTimeEdit()
            case np.bool_():
                return widgets.CheckBox()


def align_types(source: VariantType, target: VariantType | tuple):
    from prettyqt import core, gui
    from prettyqt.utils import colors

    match source:
        case core.QPoint():
            return to_point(target)
        case core.QPointF():
            return to_pointf(target)
        case core.QSize():
            return to_size(target)
        case core.QSizeF():
            return to_sizef(target)
        case core.QRect():
            return to_rect(target)
        case core.QRectF():
            return to_rectf(target)
        case gui.QColor():
            return colors.get_color(target)
        case _:
            return target


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


def to_point(point: QtCore.QPointF | PointType):
    match point:
        case (int(), int()):
            return QtCore.QPoint(*point)
        case QtCore.QPoint():
            return point
        case QtCore.QPointF():
            return point.toPointF()
        case _:
            raise TypeError(point)


def to_pointf(point: PointFType | QtCore.QPoint):
    match point:
        case (float(), float()):
            return QtCore.PointF(*point)
        case QtCore.PointF():
            return point
        case QtCore.Point():
            return point.toPointF()
        case _:
            raise TypeError(point)


def to_size(size: QtCore.QSizeF | SizeType):
    match size:
        case (int(), int()):
            return QtCore.QSize(*size)
        case QtCore.QSize():
            return size
        case QtCore.QSizeF():
            return size.toSize()
        case _:
            raise TypeError(size)


def to_sizef(size: SizeFType | QtCore.QSize):
    match size:
        case (float(), float()):
            return QtCore.QSizeF(*size)
        case QtCore.QSizeF():
            return size
        case QtCore.QSize():
            return size.toSizeF()
        case _:
            raise TypeError(size)


def to_rect(rect: QtCore.QRectF | RectType):
    match rect:
        case (int(), int(), int(), int()):
            return QtCore.QRect(*rect)
        case QtCore.QRect():
            return rect
        case QtCore.QRectF():
            return rect.toRect()
        case _:
            raise TypeError(rect)


def to_rectf(rect: RectFType | QtCore.QRect):
    match rect:
        case (float(), float(), float(), float()):
            return QtCore.QRectF(*rect)
        case QtCore.QRectF():
            return rect
        case QtCore.QRect():
            return rect.toRectF()
        case _:
            raise TypeError(rect)


def to_py_pattern(pattern: PatternAndStringType):
    from prettyqt import core

    match pattern:
        case str():
            return re.compile(pattern)
        case re.Pattern():
            return pattern
        case QtCore.QRegularExpression():
            return core.RegularExpression(pattern).to_py_pattern()


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


PatternType = re.Pattern | QtCore.QRegularExpression
PatternAndStringType = str | PatternType
JSONType = str | int | float | bool | None | dict[str, Any] | list[Any]
PathType = str | os.PathLike


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


@runtime_checkable
class IsDataclass(Protocol):
    __dataclass_fields__: ClassVar[dict]


@runtime_checkable
class IsAttrs(Protocol):
    __attrs_attrs__: ClassVar[dict]


@runtime_checkable
class IsTreeIterator(Protocol):
    @property
    def root(self):
        ...

    @property
    def _abc_impl(self):
        ...


if TYPE_CHECKING:
    from prettyqt.qt import QtGui, QtWidgets

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
