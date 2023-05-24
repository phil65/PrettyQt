from __future__ import annotations

from prettyqt import constants, core
from prettyqt.qt import QtCore


# TYPES = {
#     bool: 1,
#     int: 2,
#     str: 10,
#     float: 38,
#     QtGui.QColor: 67,
#     QtGui.QCursor: 74,
#     QtCore.QDate: 14,
#     QtCore.QSize: 21,
#     QtCore.QTime: 15,
#     list: 9,
#     QtGui.QPolygon: 71,
#     QtGui.QPolygonF: 86,
#     QtGui.QColor: 67,
#     QtGui.QColorSpace: 87,
#     QtCore.QSizeF: 22,
#     QtCore.QRectF: 20,
#     QtCore.QLine: 23,
#     QtGui.QTextLength: 77,
#     dict: 8,
#     QtGui.QIcon: 69,
#     QtGui.QPen: 76,
#     QtCore.QLineF: 24,
#     QtGui.QTextFormat: 78,
#     QtCore.QRect: 19,
#     QtCore.QPoint: 25,
#     QtCore.QUrl: 17,
#     QtCore.QRegularExpression: 44,
#     QtCore.QDateTime: 16,
#     QtCore.QPointF: 26,
#     QtGui.QPalette: 68,
#     QtGui.QFont: 64,
#     QtGui.QBrush: 66,
#     QtGui.QRegion: 72,
#     QtGui.QImage: 70,
#     QtGui.QKeySequence: 75,
#     QtWidgets.QSizePolicy: 121,
#     QtGui.QPixmap: 65,
#     QtCore.QLocale: 18,
#     QtGui.QBitmap: 73,
#     QtGui.QMatrix4x4: 81,
#     QtGui.QVector2D: 82,
#     QtGui.QVector3D: 83,
#     QtGui.QVector4D: 84,
#     QtGui.QQuaternion: 85,
#     QtCore.QEasingCurve: 29,
#     QtCore.QJsonValue: 45,
#     QtCore.QJsonDocument: 48,
#     QtCore.QModelIndex: 42,
#     QtCore.QPersistentModelIndex: 50,
#     QtCore.QUuid: 30,
#     "user": 1024,
# }


class MetaObject:
    def __init__(self, metaobject: QtCore.QMetaObject):
        self.item = metaobject

    def __getattr__(self, val):
        return getattr(self.item, val)

    def get_super_class(self) -> MetaObject | None:
        return MetaObject(klass) if (klass := self.superClass()) is not None else None

    def get_class_info(self, include_super: bool = True) -> dict[str, str]:
        start = 0 if include_super else self.item.classInfoOffset() - 1
        count = self.item.classInfoCount()
        classinfos = [self.item.classInfo(i) for i in range(start, count)]
        return {i.name(): i.value() for i in classinfos}

    def get_method(self, index: int | str) -> core.MetaMethod:
        if isinstance(index, int):
            method = core.MetaMethod(self.item.method(index))
            if not method.isValid():
                raise KeyError(index)
            return method
        for method in self.get_methods():
            if method.get_name() == index:
                return method
        raise KeyError(index)

    def get_enum(self, index: int | str) -> core.MetaEnum:
        if isinstance(index, int):
            enum = core.MetaEnum(self.item.enumerator(index))
            if not enum.isValid():
                raise KeyError(index)
            return enum
        for enumerator in self.get_enums():
            if enumerator.get_name() == index:
                return enumerator
        raise KeyError(index)

    def get_property(self, index: int | str) -> core.MetaProperty:
        if isinstance(index, int):
            prop = core.MetaProperty(self.item.property(index))
            if not prop.isValid():
                raise KeyError(index)
            return prop
        for prop in self.get_properties():
            if prop.get_name() == index:
                return prop
        raise KeyError(index)

    def get_constructor(self, index: int | str) -> core.MetaProperty:
        if isinstance(index, int):
            method = core.MetaMethod(self.item.constructor(index))
            if not method.isValid():
                raise KeyError(index)
            return method
        for method in self.get_constructors():
            if method.get_name() == index:
                return method
        raise KeyError(index)

    def get_methods(
        self,
        include_super: bool = True,
        type_filter: core.metamethod.MethodTypeStr | None = None,
        filter_shit: bool = True,
    ) -> list[core.MetaMethod]:
        start = 0 if include_super else self.item.methodOffset() - 1
        methods = [
            method
            for i in range(start, self.item.methodCount())
            if not (method := self.get_method(i)).get_name().startswith("_q_")
            or not filter_shit
        ]
        if type_filter is None:
            return methods
        else:
            return [i for i in methods if i.get_method_type() == type_filter]

    def get_enums(self, include_super: bool = True) -> list[core.MetaEnum]:
        start = 0 if include_super else self.item.enumeratorOffset() - 1
        return [self.get_enum(i) for i in range(start, self.item.enumeratorCount())]

    def get_constructors(self) -> list[core.MetaMethod]:
        count = self.item.constructorCount()
        return [core.MetaMethod(self.item.constructor(i)) for i in range(count)]

    def get_properties(
        self, include_super: bool = True, only_writable: bool = False
    ) -> list[core.MetaProperty]:
        start = 0 if include_super else self.item.propertyOffset() - 1
        count = self.item.propertyCount()
        return [
            core.MetaProperty(self.item.property(i))
            for i in range(start, count)
            if not only_writable or self.item.property(i).isWritable()
        ]

    def get_signals(self, include_super: bool = True) -> list[core.MetaMethod]:
        return self.get_methods(include_super=include_super, type_filter="signal")

    def get_slots(self, include_super: bool = True) -> list[core.MetaMethod]:
        return self.get_methods(include_super=include_super, type_filter="slot")

    def get_plain_methods(self, include_super: bool = True) -> list[core.MetaMethod]:
        return self.get_methods(include_super=include_super, type_filter="method")

    def get_meta_type(self) -> core.MetaType:
        return core.MetaType(self.metaType().id())

    def get_user_property(self) -> core.MetaProperty | None:
        prop = self.userProperty()
        return core.MetaProperty(prop) if prop.isValid() else None

    # just experimenting
    @classmethod
    def invoke_method(
        cls,
        obj: QtCore.QObject,
        method: str,
        *args,
        connection_type: constants.ConnectionTypeStr = "auto",
    ):
        conn = constants.CONNECTION_TYPE[connection_type]
        args = tuple(core.Q_ARG(type(arg), arg) for arg in args)
        return cls.invokeMethod(obj, method, conn, *args)

    def get_new_instance(self, *args, **kwargs):
        args = tuple(core.Q_ARG(type(i), i) for i in args)
        kwargs = {k: core.Q_ARG(type(v), v) for k, v in kwargs.items()}
        # requires QtCore.QGenericArgumentHolder for PySide6
        self.newInstance(*args, **kwargs)


if __name__ == "__main__":
    from prettyqt import widgets

    metaobj = widgets.AbstractItemView.get_static_metaobject()
    print(metaobj.get_methods())
