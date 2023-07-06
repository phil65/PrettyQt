from __future__ import annotations

from abc import ABCMeta
from collections.abc import Sequence
import datetime
import enum
import os
import pathlib
import re

from typing import TYPE_CHECKING, Any, ClassVar, Protocol, TypeVar, runtime_checkable
from urllib import parse

import dateutil.parser

from prettyqt.qt import QtCore


class QABCMeta(type(QtCore.QObject), ABCMeta):
    """Metaclass, mainly used for inheriting from MutableMapping."""


class Singleton(type(QtCore.QObject), type):
    """Metaclass to create a singleton."""

    def __init__(cls, name, bases, dct):
        super().__init__(name, bases, dct)
        cls.instance = None

    def __call__(cls, *args, **kw):
        if cls.instance is None:
            cls.instance = super().__call__(*args, **kw)
        return cls.instance


Indexer = tuple[slice | int, slice | int]
IndexerOrInt = Indexer | int
SingleResultIndexer = int | tuple[int, int]
MultiResultIndexer = tuple[slice, int] | tuple[int, slice] | tuple[slice, slice]

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
    from prettyqt import core
    from prettyqt.qt import QtGui, QtWidgets

    UrlType = str | QtCore.QUrl
    PointType = tuple[int, int] | QtCore.QPoint
    PointFType = tuple[int | float, int | float] | QtCore.QPointF
    SizeType = tuple[int, int] | QtCore.QSize | int
    SizeFType = tuple[int | float, int | float] | QtCore.QSizeF
    MarginsType = tuple[int, int, int, int] | tuple[int, int] | int | QtCore.QMargins
    MarginsFType = (
        tuple[int | float, int | float, int | float, int | float]
        | tuple[int | float, int | float]
        | int
        | float
        | QtCore.QMarginsF
    )
    RectType = tuple[int, int, int, int] | QtCore.QRect
    RectFType = tuple[int | float, int | float, int | float, int | float] | QtCore.QRectF
    Vector3DType = (
        tuple[int | float, int | float, int | float]
        | QtCore.QPoint
        | QtCore.QPointF
        | QtGui.QVector2D
        | QtGui.QVector3D
        | QtGui.QVector4D
    )
    LineType = tuple[int, int] | QtCore.QLine
    LineFType = tuple[float, float] | QtCore.QLineF | QtCore.QLine
    SemanticVersionType = str | QtCore.QVersionNumber | tuple[int, int, int]
    IconType = QtGui.QIcon | str | pathlib.Path | None
    ByteArrayType = str | bytes | QtCore.QByteArray
    TimeType = QtCore.QTime | datetime.time | str | tuple[int, int, int]
    DateType = QtCore.QDate | datetime.date | str | tuple[int, int, int]
    DateTimeType = (
        QtCore.QDateTime | datetime.datetime | str | tuple[int, int, int, int, int, int]
    )
    KeySequenceType = QtGui.QKeySequence | QtCore.QKeyCombination | str | None
    # ContainerType = Union[widgets.Layout, widgets.Splitter]
    TransformType = (
        QtGui.QTransform
        | tuple[float, float, float, float, float, float, float, float, float]
        | tuple[float, float, float, float, float, float]
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
        case gui.QBrush():
            # TODO: can also be gradient
            val = val.color()
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
        case slice() | range():
            return f"({val.start=}, {val.stop=}, {val.step=}"
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


def get_editor_for_value_list(ls: Sequence, parent=None):
    from prettyqt import widgets

    container = widgets.Widget(parent)
    container.set_layout("vertical")
    editors = [get_editor_for_value(val, parent=container) for val in ls]
    container.box.add(editors)
    container.set_window_flags("tool")
    return container


def get_editor_for_value(val, parent=None):
    """Returns an editor for given value.

    Functions checks for type and returns an appropriate editor.
    The returned editor is guaranteed to have a get_value and set_value method
    which can be used to the given value.

    Arguments:
        val: Any value type
        parent: parent widget for editor
    """
    from prettyqt import core, custom_widgets, gui, widgets

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
        case (int(), *_):
            return custom_widgets.ListInput(parent=parent, typ=int)
        case (float(), *_):
            return custom_widgets.ListInput(parent=parent, typ=float)
        case (str(), *_):
            return custom_widgets.StringListEdit(parent=parent)
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
        case gui.QBrush():
            return custom_widgets.BrushEdit(parent=parent)
        case widgets.QSizePolicy():
            return custom_widgets.SizePolicyEdit(parent=parent)
        case core.QUrl():
            return custom_widgets.UrlLineEdit(parent=parent)
        case gui.QPalette():
            return custom_widgets.PaletteEdit(parent=parent)
        case gui.QCursor():
            return custom_widgets.CursorEdit(parent=parent)
        case gui.QIcon():
            return custom_widgets.IconEdit(parent=parent)
        case core.QLocale():
            return custom_widgets.LocaleEdit(parent=parent)
        case slice():
            return custom_widgets.SliceEdit(parent=parent)
        case range():
            return custom_widgets.RangeEdit(parent=parent)
        # case QtCore.QRectF():  # todo
        #     return custom_widgets.RectEdit(parent=parent)
    try:
        import numpy as np
    except ImportError:
        pass
    else:
        match val:
            case np.floating():
                return custom_widgets.FloatLineEdit(parent=parent)
            case np.integer():
                return custom_widgets.IntLineEdit(parent=parent)
            case np.str_():
                return widgets.LineEdit(parent=parent)
            case np.datetime64():
                return widgets.DateTimeEdit(parent=parent)
            case np.bool_():
                return widgets.CheckBox(parent=parent)


T = TypeVar("T")


def align_types(source: T, target: VariantType | tuple) -> T:
    """Align target to the type of source."""
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
            return colors.get_color(target).as_qt()
        case _:
            return target


def make_qtype(obj):
    """Cast a subclassed PrettyQt instance to its orginal Qt Type."""
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
        case (int() | float(), int() | float()):
            return QtCore.QPointF(*point)
        case QtCore.QPointF():
            return point
        case QtCore.QPoint():
            return point.toPointF()
        case _:
            raise TypeError(point)


def to_size(size: QtCore.QSizeF | SizeType):
    match size:
        case (int(), int()):
            return QtCore.QSize(*size)
        case int():
            return QtCore.QSize(size, size)
        case QtCore.QSize():
            return size
        case QtCore.QSizeF():
            return size.toSize()
        case _:
            raise TypeError(size)


def to_sizef(size: SizeFType | QtCore.QSize):
    match size:
        case (int() | float(), int() | float()):
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
        case (int() | float(), int() | float(), int() | float(), int() | float()):
            return QtCore.QRectF(*rect)
        case QtCore.QRectF():
            return rect
        case QtCore.QRect():
            return rect.toRectF()
        case _:
            raise TypeError(rect)


def to_vector3d(vector: Vector3DType):
    from prettyqt import core, gui

    match vector:
        case (int() | float(), int() | float(), int() | float()):
            return gui.QVector3D(*vector)
        case gui.QVector3D():
            return vector
        case gui.QVector2D() | gui.QVector4D() | core.QPoint() | core.QPointF():
            return gui.QVector3D(vector)
        case _:
            raise TypeError(vector)


def to_url(url: UrlType | None) -> QtCore.QUrl:
    match url:
        case os.PathLike():
            return QtCore.QUrl.fromLocalFile(os.fspath(url))
        case str():
            return QtCore.QUrl(url)
        case None:
            return QtCore.QUrl()
        case QtCore.QUrl():
            return url
        case parse.ParseResult():
            return QtCore.QUrl(url.geturl())
        case _:
            raise TypeError(url)


def to_local_url(url: UrlType | os.PathLike | None) -> QtCore.QUrl:
    # TODO: need to check whether we should merge to_local_url and to_url
    # core.Url.from_user_input() perhaps a good option, too?
    match url:
        case os.PathLike():
            return QtCore.QUrl.fromLocalFile(os.fspath(url))
        case str():
            return QtCore.QUrl.fromLocalFile(url)
        case None:
            return QtCore.QUrl()
        case QtCore.QUrl():
            return url
        case _:
            raise TypeError(url)


def to_bytearray(arr: str | bytes | QtCore.QByteArray) -> QtCore.QByteArray:
    match arr:
        case str():
            return QtCore.QByteArray(arr.encode())
        case bytes():
            return QtCore.QByteArray(arr)
        case QtCore.QByteArray():
            return arr
        case _:
            raise TypeError(arr)


def to_margins(margins: MarginsType | QtCore.QMarginsF | None) -> QtCore.QMargins:
    match margins:
        case (int() as x, int() as y):
            return QtCore.QMargins(x, y, x, y)
        case (int() as left, int() as top, int() as right, int() as bottom):
            return QtCore.QMargins(left, top, right, bottom)
        case QtCore.QMargins():
            return margins
        case QtCore.QMarginsF():
            return margins.toMargins()
        case int() as x:
            return QtCore.QMargins(x, x, x, x)
        case None:
            return QtCore.QMargins(0, 0, 0, 0)
        case _:
            raise TypeError(margins)


def to_marginsf(margins: MarginsFType | QtCore.QMargins | None) -> QtCore.QMarginsF:
    match margins:
        case (int() | float() as x, int() | float() as y):
            return QtCore.QMarginsF(x, y, x, y)
        case (
            int() | float() as left,
            int() | float() as top,
            int() | float() as right,
            int() | float() as bottom,
        ):
            return QtCore.QMarginsF(left, top, right, bottom)
        case QtCore.QMarginsF():
            return margins
        case QtCore.QMargins():
            return margins.toMarginsF()
        case int() | float() as x:
            return QtCore.QMarginsF(x, x, x, x)
        case None:
            return QtCore.QMarginsF(0, 0, 0, 0)
        case _:
            raise TypeError(margins)


def to_datetime(date_time: DateTimeType):
    match date_time:
        case None:
            return QtCore.QDateTime()
        case (int(), int(), int(), int(), int(), int()):
            date_ = QtCore.QDate(*date_time[:3])
            time_ = QtCore.QTime(*date_time[3:])
            return QtCore.QDateTime(date_, time_)
        case str():
            return dateutil.parser.parse(date_time)
        case QtCore.QDateTime() | datetime.datetime():
            return date_time
        case _:
            raise TypeError(date_time)


def to_date(value: DateType):
    match value:
        case None:
            return QtCore.QDate()
        case (int(), int(), int()):
            return QtCore.QDate(*value)
        case str():
            return QtCore.QDate.fromString(value)
        case QtCore.QDate() | datetime.date():
            return value
        case _:
            raise TypeError(value)


def to_time(value: TimeType):
    from prettyqt import core

    match value:
        case str():
            val = core.Time.from_string(value)
            if not val.isValid():
                raise ValueError(value)
            return val
        case (int(), int(), int()):
            return QtCore.QTime(*value)
        case core.QTime():
            return core.Time(value)
        case core.QDateTime():
            return core.DateTime(value).get_time()
        case datetime.time():
            return core.Time(value)
        case datetime.datetime():
            return core.DateTime(value).get_time()
        case _:
            raise TypeError(value)


def to_linef(line: LineFType):
    match line:
        case QtCore.QLine():
            return QtCore.QLineF(line)
        case tuple():
            return QtCore.QLineF(*line)
        case QtCore.QLineF():
            return line
        case _:
            raise TypeError(line)


def to_py_pattern(pattern: PatternAndStringType):
    from prettyqt import core

    match pattern:
        case str():
            return re.compile(pattern)
        case re.Pattern():
            return pattern
        case QtCore.QRegularExpression():
            return core.RegularExpression(pattern).to_py_pattern()
        case _:
            raise TypeError(pattern)


def to_regular_expression(
    pattern: PatternAndStringType,
    flag: core.regularexpression.PatternOptionStr
    | core.RegularExpression.PatternOption
    | None = None,
):
    from prettyqt import core

    if flag is None:
        flag = core.RegularExpression.PatternOption.NoPatternOption
    else:
        flag = core.regularexpression.PATTERN_OPTIONS.get_enum_value(flag)
    match pattern:
        case str():
            return core.RegularExpression(pattern, flag)
        case re.Pattern():
            return core.RegularExpression(pattern)
        case QtCore.QRegularExpression():
            return core.RegularExpression(pattern)
        case _:
            raise TypeError(pattern)


def to_transform(transform: TransformType):
    match transform:
        case tuple():
            return QtGui.QTransform(*transform)
        case QtGui.QTransform():
            return transform
        case _:
            raise TypeError(transform)


def to_keysequence(sequence: KeySequenceType):
    from prettyqt import gui

    match sequence:
        case None:
            return gui.KeySequence("")
        case QtCore.QKeyCombination():
            return gui.KeySequence(sequence)
        case gui.QKeySequence():
            return sequence
        case str():
            return gui.KeySequence(sequence, gui.KeySequence.SequenceFormat.PortableText)
        case _:
            raise TypeError(sequence)


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
