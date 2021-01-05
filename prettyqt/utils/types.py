import pathlib
from typing import Any, Dict, List, Union

from prettyqt.qt import QtCore, QtGui, QtWidgets


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
    None,
]

Variant = Union[VariantType, List[VariantType], Dict[str, VariantType]]
