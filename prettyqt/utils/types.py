from __future__ import annotations

import datetime
import os
import pathlib
from typing import TYPE_CHECKING, Any, Protocol, Union


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

    ColorType = Union[
        str,
        int,
        QtCore.Qt.GlobalColor,
        QtGui.QColor,
        tuple[int, int, int],
        tuple[int, int, int, int],
        None,
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
