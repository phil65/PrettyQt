from __future__ import annotations

import pathlib
from typing import TYPE_CHECKING, Any, Dict, List, Protocol, Union


if TYPE_CHECKING:
    from prettyqt.qt import QtCore, QtGui, QtWebEngineWidgets, QtWidgets

    JSONType = Union[str, int, float, bool, None, Dict[str, Any], List[Any]]

    IconType = Union[QtGui.QIcon, str, pathlib.Path, None]

    ColorType = Union[str, int, QtCore.Qt.GlobalColor, QtGui.QColor, tuple, None]
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

    Variant = Union[VariantType, List[VariantType], Dict[str, VariantType]]

    class Validatable(Protocol):
        """An object with an isValid() method (e.g. QUrl)."""

        def isValid(self) -> bool:
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
        QtWebEngineWidgets.QWebEngineHistory,
    ]
