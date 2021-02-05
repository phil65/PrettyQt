from __future__ import annotations

from prettyqt import core
from prettyqt.qt import QtCore, QtGui, QtWidgets


TYPES = {
    bool: 1,
    int: 2,
    str: 10,
    float: 38,
    QtGui.QColor: 67,
    QtGui.QCursor: 74,
    QtCore.QDate: 14,
    QtCore.QSize: 21,
    QtCore.QTime: 15,
    list: 9,
    QtGui.QPolygon: 71,
    QtGui.QPolygonF: 86,
    QtGui.QColor: 67,
    QtGui.QColorSpace: 87,
    QtCore.QSizeF: 22,
    QtCore.QRectF: 20,
    QtCore.QLine: 23,
    QtGui.QTextLength: 77,
    dict: 8,
    QtGui.QIcon: 69,
    QtGui.QPen: 76,
    QtCore.QLineF: 24,
    QtGui.QTextFormat: 78,
    QtCore.QRect: 19,
    QtCore.QPoint: 25,
    QtCore.QUrl: 17,
    QtCore.QRegularExpression: 44,
    QtCore.QDateTime: 16,
    QtCore.QPointF: 26,
    QtGui.QPalette: 68,
    QtGui.QFont: 64,
    QtGui.QBrush: 66,
    QtGui.QRegion: 72,
    QtGui.QImage: 70,
    QtGui.QKeySequence: 75,
    QtWidgets.QSizePolicy: 121,
    QtGui.QPixmap: 65,
    QtCore.QLocale: 18,
    QtGui.QBitmap: 73,
    QtGui.QMatrix4x4: 81,
    QtGui.QVector2D: 82,
    QtGui.QVector3D: 83,
    QtGui.QVector4D: 84,
    QtGui.QQuaternion: 85,
    QtCore.QEasingCurve: 29,
    QtCore.QJsonValue: 45,
    QtCore.QJsonDocument: 48,
    QtCore.QModelIndex: 42,
    QtCore.QPersistentModelIndex: 50,
    QtCore.QUuid: 30,
    "user": 1024,
}


class MetaObject:
    def __init__(self, metaobject: QtCore.QMetaObject):
        self.item = metaobject

    def get_method(self, index: int | str) -> core.MetaMethod:
        if isinstance(index, int):
            return self.get_methods()[index]
        else:
            for method in self.get_methods():
                if method.get_name() == index:
                    return method
            raise KeyError(index)

    def get_enum(self, index: int | str) -> core.MetaEnum:
        if isinstance(index, int):
            return self.get_enums()[index]
        else:
            for enumerator in self.get_enums():
                if enumerator.get_name() == index:
                    return enumerator
            raise KeyError(index)

    def get_methods(
        self,
        include_super: bool = True,
        type_filter: core.metamethod.MethodTypeStr | None = None,
    ) -> list[core.MetaMethod]:
        start = 0 if include_super else self.item.methodOffset()
        methods = [
            core.MetaMethod(self.item.method(i))
            for i in range(start, self.item.methodCount())
        ]
        if type_filter is None:
            return methods
        else:
            return [i for i in methods if i.get_method_type() == type_filter]

    def get_enums(self, include_super: bool = True) -> list[core.MetaEnum]:
        start = 0 if include_super else self.item.enumeratorOffset()
        return [
            core.MetaEnum(self.item.enumerator(i))
            for i in range(start, self.item.enumeratorCount())
        ]

    def get_constructors(self) -> list[core.MetaMethod]:
        return [
            core.MetaMethod(self.item.constructor(i))
            for i in range(self.item.constructorCount())
        ]

    def get_properties(self, include_super: bool = True) -> list[core.MetaProperty]:
        start = 0 if include_super else self.item.propertyOffset()
        return [
            core.MetaProperty(self.item.property(i))
            for i in range(start, self.item.propertyCount())
        ]

    def get_signals(self, include_super: bool = True) -> list[core.MetaMethod]:
        return [
            i
            for i in self.get_methods(include_super=include_super)
            if i.get_method_type() == "signal"
        ]


if __name__ == "__main__":
    metaobj = core.Object.get_metaobject()
    print(metaobj.get_signals())
