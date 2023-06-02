from __future__ import annotations

import logging
from collections.abc import Callable
from typing import Any

from prettyqt import constants, core
from prettyqt.qt import QtCore
from prettyqt.utils import datatypes

logger = logging.getLogger(__name__)

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
        """Get SuperClass MetaObject."""
        return MetaObject(klass) if (klass := self.superClass()) is not None else None

    def get_name(self) -> str:
        """Get MetaObject class name."""
        return self.className()

    def get_class_info(self, include_super: bool = True) -> dict[str, str]:
        """Get MetaObject class info."""
        start = 0 if include_super else self.item.classInfoOffset() - 1
        count = self.item.classInfoCount()
        classinfos = [self.item.classInfo(i) for i in range(start, count)]
        return {i.name(): i.value() for i in classinfos}

    def get_method(self, index: int | str) -> core.MetaMethod:
        """Get MetaMethod based on index or name."""
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
        """Get MetaEnum based on index or name."""
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
        """Get MetaProperty based on index or name."""
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
        """Get ctor MetaMethod based on index or name."""
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
        """Get all MetaMethods based on given criteria."""
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
        """Get all MetaEnums based on given criteria."""
        start = 0 if include_super else self.item.enumeratorOffset() - 1
        return [self.get_enum(i) for i in range(start, self.item.enumeratorCount())]

    def get_constructors(self) -> list[core.MetaMethod]:
        """Get all ctor MetaMethods."""
        count = self.item.constructorCount()
        return [core.MetaMethod(self.item.constructor(i)) for i in range(count)]

    def get_properties(
        self, include_super: bool = True, only_writable: bool = False
    ) -> list[core.MetaProperty]:
        """Get all MetaProperties based on given criteria."""
        start = 0 if include_super else self.item.propertyOffset() - 1
        count = self.item.propertyCount()
        return [
            core.MetaProperty(self.item.property(i))
            for i in range(start, count)
            if not only_writable or self.item.property(i).isWritable()
        ]

    def get_property_values(
        self, qobject: QtCore.QObject, cast_types: bool = False
    ) -> dict[str, Any]:
        """Get a dictionary containing all MetaProperties values from given qobject."""
        vals = {prop.get_name(): prop.read(qobject) for prop in self.get_properties()}
        if cast_types:
            return {k: datatypes.make_serializable(v) for k, v in vals.items()}
        else:
            return vals

    def get_signals(
        self, include_super: bool = True, only_notifiers: bool = False
    ) -> list[core.MetaMethod]:
        """Get all signal MetaMethods based on given criteria."""
        if only_notifiers:
            return [
                prop.get_notify_signal()
                for prop in self.get_properties(include_super)
                if prop.hasNotifySignal()
            ]
        else:
            return self.get_methods(include_super=include_super, type_filter="signal")

    def get_slots(self, include_super: bool = True) -> list[core.MetaMethod]:
        """Get all slot MetaMethods based on given criteria."""
        return self.get_methods(include_super=include_super, type_filter="slot")

    def get_plain_methods(self, include_super: bool = True) -> list[core.MetaMethod]:
        """Get all plain MetaMethods based on given criteria."""
        return self.get_methods(include_super=include_super, type_filter="method")

    def get_meta_type(self) -> core.MetaType:
        """Get Meta type of this MetaObject."""
        return core.MetaType(self.metaType().id())

    def get_user_property(self) -> core.MetaProperty | None:
        """Get MetaProperty marked as userprop."""
        return core.MetaProperty(p) if (p := self.userProperty()).isValid() else None

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

    def connect_signals(
        self, qobject: QtCore.QObject, fn: Callable, only_notifiers: bool = False
    ) -> list[QtCore.QMetaObject.Connection]:
        """Connect all signals of a given qobject to fn."""
        handles = []
        for signal in self.get_signals(only_notifiers=only_notifiers):
            signal_name = signal.get_name()
            signal_instance = qobject.__getattribute__(signal_name)
            handle = signal_instance.connect(fn)
            handles.append(handle)
        logger.debug(f"connected {len(handles)} signals to {fn}.")
        return handles

    def copy(self, widget, forward_signals: bool = True):
        """Create a copy of given widget."""
        try:
            new = type(widget)()
        except TypeError:
            # this should should cover most cases.
            new = type(widget)(widget.orientation())
        for prop in self.get_properties(only_writable=True):
            val = prop.read(widget)
            prop.write(new, val)
        # MetaObject can return non-existing signals, dont know why.
        # also filter out duplicates.
        signal_names = {
            s.get_name() for s in self.get_signals() if hasattr(widget, s.get_name())
        }
        if forward_signals:
            for signal_name in signal_names:
                own_signal = widget.__getattribute__(signal_name)
                new_signal = new.__getattribute__(signal_name)
                # own_signal.connect(new_signal)
                new_signal.connect(own_signal)
        logger.debug(f"copied {widget!r}")
        return new

    def get_property_class_affiliations(self) -> dict[str, list[core.MetaProperty]]:
        """Get a mapping of class -> property affiliations."""
        mapper = {}
        metaclass = self
        while metaclass is not None:
            mapper[metaclass.get_name()] = [
                metaclass.get_property(i)
                for i in range(metaclass.propertyOffset(), metaclass.propertyCount())
            ]
            metaclass = metaclass.get_super_class()
        return mapper


if __name__ == "__main__":
    from prettyqt import widgets

    app = widgets.app()
    h = widgets.HeaderView("horizontal")
    metaobj = h.get_metaobject()
    kls = metaobj.get_property_class_affiliations()
    # print(kls)
