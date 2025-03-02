from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any, TypeVar

from prettyqt import constants, core
from prettyqt.utils import datatypes, helpers


if TYPE_CHECKING:
    from collections.abc import Callable


T = TypeVar("T", bound=core.QObject)

logger = logging.getLogger(__name__)

# TYPES = {
#     bool: 1,
#     int: 2,
#     str: 10,
#     float: 38,
#     QtGui.QColor: 67,
#     QtGui.QCursor: 74,
#     core.QDate: 14,
#     core.QSize: 21,
#     core.QTime: 15,
#     list: 9,
#     QtGui.QPolygon: 71,
#     QtGui.QPolygonF: 86,
#     QtGui.QColor: 67,
#     QtGui.QColorSpace: 87,
#     core.QSizeF: 22,
#     core.QRectF: 20,
#     core.QLine: 23,
#     QtGui.QTextLength: 77,
#     dict: 8,
#     QtGui.QIcon: 69,
#     QtGui.QPen: 76,
#     core.QLineF: 24,
#     QtGui.QTextFormat: 78,
#     core.QRect: 19,
#     core.QPoint: 25,
#     core.QUrl: 17,
#     core.QRegularExpression: 44,
#     core.QDateTime: 16,
#     core.QPointF: 26,
#     QtGui.QPalette: 68,
#     QtGui.QFont: 64,
#     QtGui.QBrush: 66,
#     QtGui.QRegion: 72,
#     QtGui.QImage: 70,
#     QtGui.QKeySequence: 75,
#     QtWidgets.QSizePolicy: 121,
#     QtGui.QPixmap: 65,
#     core.QLocale: 18,
#     QtGui.QBitmap: 73,
#     QtGui.QMatrix4x4: 81,
#     QtGui.QVector2D: 82,
#     QtGui.QVector3D: 83,
#     QtGui.QVector4D: 84,
#     QtGui.QQuaternion: 85,
#     core.QEasingCurve: 29,
#     core.QJsonValue: 45,
#     core.QJsonDocument: 48,
#     core.QModelIndex: 42,
#     core.QPersistentModelIndex: 50,
#     core.QUuid: 30,
#     "user": 1024,
# }


class MetaObject:
    """Contains meta-information about Qt objects."""

    def __init__(self, metaobject: core.QMetaObject):
        self.item = metaobject

    def __getattr__(self, val):
        return getattr(self.item, val)

    def get_super_class(self) -> MetaObject | None:
        """Get SuperClass MetaObject."""
        return MetaObject(klass) if (klass := self.superClass()) is not None else None

    def get_all_super_classes(self) -> list[MetaObject]:
        """Get SuperClass MetaObject."""
        klasses = []
        while klass := self.superClass():
            klasses.append(MetaObject(klass))
        return klasses

    def get_name(self) -> str:
        """Get MetaObject class name."""
        return self.className()

    def get_class_info(self, include_super: bool = True) -> dict[str, str]:
        """Get MetaObject class info.

        Arguments:
            include_super: Whether to include class info from parent classes.
        """
        start = 0 if include_super else self.item.classInfoOffset()
        count = self.item.classInfoCount()
        classinfos = [self.item.classInfo(i) for i in range(start, count)]
        return {i.name(): i.value() for i in classinfos}

    def get_method(self, index: int | str) -> core.MetaMethod:
        """Get MetaMethod based on index or name.

        Arguments:
            index: index or method name
        """
        if isinstance(index, int):
            method = core.MetaMethod(self.item.method(index))
            if not method.isValid():
                raise KeyError(index)
            return method
        for method in self.get_methods():
            if method.get_name() in [index, helpers.to_lower_camel(index)]:
                return method
        raise KeyError(index)

    def get_enum(self, index: int | str) -> core.MetaEnum:
        """Get MetaEnum based on index or name.

        Arguments:
            index: index or Enum name
        """
        if isinstance(index, int):
            enum = core.MetaEnum(self.item.enumerator(index))
            if not enum.isValid():
                raise KeyError(index)
            return enum
        for enumerator in self.get_enums():
            if enumerator.get_name() in [index, helpers.to_lower_camel(index)]:
                return enumerator
        raise KeyError(index)

    def has_property(self, name: str):
        """Check if a property with given name exists.

        Only checks for non-dynamic properties.

        Arguments:
            name: property name
        """
        try:
            self.get_property(name)
        except KeyError:
            return False
        else:
            return True

    def get_property(self, index: int | str) -> core.MetaProperty:
        """Get MetaProperty based on index or name.

        Only returns non-dynamic properties.

        Arguments:
            index: index or property name
        """
        if isinstance(index, int):
            prop = core.MetaProperty(self.item.property(index))
            if not prop.isValid():
                raise KeyError(index)
            return prop
        for prop in self.get_properties():
            if prop.get_name() in [index, helpers.to_lower_camel(index)]:
                return prop
        raise KeyError(index)

    def get_constructor(self, index: int | str) -> core.MetaMethod:
        """Get ctor MetaMethod based on index or name.

        Arguments:
            index: index or constructor name
        """
        if isinstance(index, int):
            method = core.MetaMethod(self.item.constructor(index))
            if not method.isValid():
                raise KeyError(index)
            return method
        for method in self.get_constructors():
            if method.get_name() in [index, helpers.to_lower_camel(index)]:
                return method
        raise KeyError(index)

    def get_methods(
        self,
        include_super: bool = True,
        type_filter: core.metamethod.MethodTypeStr | None = None,
        filter_internal: bool = True,
    ) -> list[core.MetaMethod]:
        """Get all MetaMethods based on given criteria.

        Arguments:
            include_super: Whether to include Methods from parent classes
            type_filter: Method type to filter for.
            filter_internal: Filter Qt-internal methods
        """
        start = 0 if include_super else self.item.methodOffset()
        methods = [
            method
            for i in range(start, self.item.methodCount())
            if not (method := self.get_method(i)).get_name().startswith("_q_")
            or not filter_internal
        ]
        if type_filter is None:
            return methods
        return [i for i in methods if i.get_method_type() == type_filter]

    def get_enums(self, include_super: bool = True) -> list[core.MetaEnum]:
        """Get all MetaEnums based on given criteria.

        Arguments:
            include_super: Whether to include Enums from parent classes.
        """
        start = 0 if include_super else self.item.enumeratorOffset()
        return [self.get_enum(i) for i in range(start, self.item.enumeratorCount())]

    def get_constructors(self) -> list[core.MetaMethod]:
        """Get all ctor MetaMethods."""
        count = self.item.constructorCount()
        return [core.MetaMethod(self.item.constructor(i)) for i in range(count)]

    def get_properties(
        self,
        include_super: bool = True,
        only_writable: bool = False,
        only_stored: bool = False,
        only_bindable: bool = False,
        only_designable: bool = False,
        only_final: bool = False,
        only_required: bool = False,
        only_enum_type: bool = False,
        only_flag_type: bool = False,
        only_with_notifiers: bool = False,
        only_with_type_name: str = "",
    ) -> list[core.MetaProperty]:
        """Get all MetaProperties based on given criteria.

        Arguments:
            include_super: Whether to include properties from parent classes,
            only_writable: Whether to filter for writable properties.
            only_stored: Whether to filter for stored properties.
            only_bindable: Whether to filter for bindable properties.
            only_designable: Whether to filter for designable properties.
            only_final: Whether to filter for final properties.
            only_required: Whether to filter for required properties.
            only_enum_type: Whether to filter for Enum type properties.
            only_flag_type: Whether to filter for Flag_type properties.
            only_with_notifiers: Whether to filter for properties with notifier.
            only_with_type_name: Only include properties with given give name as type.
        """
        start = 0 if include_super else self.item.propertyOffset()
        count = self.item.propertyCount()
        prop_list = []
        for i in range(start, count):
            prop = self.item.property(i)
            if (
                (only_writable and not prop.isWritable())
                or (only_stored and not prop.isStored())
                or (only_bindable and not prop.isBindable())
                or (only_designable and not prop.isDesignable())
                or (only_final and not prop.isFinal())
                or (only_required and not prop.isRequired())
                or (only_enum_type and not prop.isEnumType())
                or (only_flag_type and not prop.isFlagType())
                or (only_with_notifiers and not prop.hasNotifier())
                or (only_with_type_name and prop.typeName() != only_with_type_name)
            ):
                continue
            prop_list.append(core.MetaProperty(prop))
        return prop_list

    def get_property_values(
        self, qobject: core.QObject, cast_types: bool = False
    ) -> dict[str, Any]:
        """Get a dictionary containing all MetaProperties values from given qobject.

        Arguments:
            qobject: QObject to get properties from
            cast_types: Whether to cast types to PrettyQt classes.
        """
        vals = {prop.get_name(): prop.read(qobject) for prop in self.get_properties()}
        if cast_types:
            return {k: datatypes.make_serializable(v) for k, v in vals.items()}
        return vals

    def get_signals(
        self, include_super: bool = True, only_notifiers: bool = False
    ) -> list[core.MetaMethod]:
        """Get all signal MetaMethods based on given criteria.

        Arguments:
            include_super: Whether to include Signals from parent classes
            only_notifiers: Whether to filter for property notifier signals
        """
        if only_notifiers:
            return [  # type: ignore
                prop.get_notify_signal()
                for prop in self.get_properties(include_super)
                if prop.hasNotifySignal()
            ]
        return self.get_methods(include_super=include_super, type_filter="signal")

    def get_slots(self, include_super: bool = True) -> list[core.MetaMethod]:
        """Get all slot MetaMethods based on given criteria.

        Arguments:
            include_super: Whether to include Slots from parent classes
        """
        return self.get_methods(include_super=include_super, type_filter="slot")

    def get_plain_methods(self, include_super: bool = True) -> list[core.MetaMethod]:
        """Get all plain MetaMethods based on given criteria.

        Arguments:
            include_super: Whether to include plain methods from parent classes
        """
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
        obj: core.QObject,
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
        # requires core.QGenericArgumentHolder for PySide6
        self.newInstance(*args, **kwargs)

    def connect_signals(
        self,
        source_qobject: core.QObject,
        fn_or_qobject: Callable | core.QObject,
        only_notifiers: bool = False,
    ) -> list[core.QMetaObject.Connection]:
        """Connect all signals of a given qobject.

        Either connect all signals to a function or connect each signal
        to the corresponding signal of the receiver.
        """
        handles = []
        for signal in self.get_signals(only_notifiers=only_notifiers):
            signal_name = signal.get_name()
            if not hasattr(source_qobject, signal_name):
                # PyQt6 reports applicationNameChanged for QCoreApplication,
                # but it doesnt exist...
                logger.warning("Signal %r does not exist.", signal_name)
                continue
            signal_instance = getattr(source_qobject, signal_name)
            slot = (
                getattr(fn_or_qobject, signal_name)
                if isinstance(fn_or_qobject, core.QObject)
                else fn_or_qobject
            )
            handle = signal_instance.connect(slot)
            handles.append(handle)
        logger.debug("connected %s signals to %s.", len(handles), fn_or_qobject)
        return handles

    def copy(self, qobject: T, forward_signals: bool = True) -> T:
        """Create a copy of given QObject.

        Arguments:
            qobject: QObject to create a copied instance for.
            forward_signals: Whether to connect all signals from qobject to the new
                             instance.
        """
        try:
            new = type(qobject)()
        except TypeError:
            # this should should cover most cases.
            new = type(qobject)(qobject.orientation())
        for prop in self.get_properties(only_writable=True):
            val = prop.read(qobject)
            prop.write(new, val)
        if forward_signals:
            self.connect_signals(new, qobject)
        logger.debug("copied %r", qobject)
        return new

    @classmethod
    def copy_properties_to(cls, source: core.QObject, target: core.QObject):
        """Sets all properties of target to value of source.

        Only sets properties which exist for both QObjects.

        Arguments:
            source: Source QObject
            target: Target QObject
        """
        source_metaobj = cls(source.metaObject())
        target_metaobj = cls(target.metaObject())
        for prop in target_metaobj.get_properties(only_writable=True):
            if source_metaobj.has_property(prop_name := prop.get_name()):
                target.setProperty(prop_name, source.property(prop_name))

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
