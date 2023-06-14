from __future__ import annotations

from collections import defaultdict
from collections.abc import Callable, Generator, Sequence
import contextlib

# import inspect
import itertools
import logging
import re
from typing import TYPE_CHECKING, Any, TypeVar, get_args
import types

from prettyqt import constants, core
from prettyqt.qt import QtCore
from prettyqt.utils import datatypes, listdelegators, helpers


if TYPE_CHECKING:
    from prettyqt import eventfilters

T = TypeVar("T", bound=QtCore.QObject)

counter_dict: defaultdict = defaultdict(itertools.count)

logger = logging.getLogger(__name__)


class ObjectMixin:
    _properties: list = []
    _signals: list = []

    def __new__(cls, *args, **kwargs):
        """Cache a list of properties and signals as class attribute."""
        if issubclass(cls, QtCore.QObject) and not cls._properties:
            metaobj = core.MetaObject(cls.staticMetaObject)
            cls._properties = [i.get_name() for i in metaobj.get_properties()]
            cls._signals = [i.get_name() for i in metaobj.get_signals()]
            return super().__new__(cls, *args, **kwargs)
        return super().__new__(cls)

    def __init__(self, *args, **kwargs):
        self._eventfilters = set()
        # klass = type(self)
        # if issubclass(klass, QtCore.QObject) and klass not in _properties:
        #     metaobj = core.MetaObject(klass.staticMetaObject)
        #     _properties[klass] = [i.get_name() for i in metaobj.get_properties()]
        #     _signals[klass] = [i.get_name() for i in metaobj.get_signals()]
        new = {}
        if kwargs:
            mapper = self._get_map()
            for k, v in kwargs.items():
                # this allows snake_case naming.
                camel_k = helpers.to_lower_camel(k)
                if camel_k != k and camel_k in kwargs:
                    logger.warning(f"{k} defined twice: {v} / {kwargs[camel_k]}")
                # allow str values instead of enum
                if camel_k in mapper and isinstance(v, str):
                    new[camel_k] = mapper[camel_k][v]
                # allow str values for common icon kwargs
                elif k in {"window_icon", "icon"} and isinstance(v, str):
                    from prettyqt import iconprovider

                    new[camel_k] = iconprovider.get_icon(v)
                # kwargs which need camel-casing
                elif camel_k in self._properties or camel_k in self._signals:
                    new[camel_k] = v
                else:
                    new[k] = v
        super().__init__(*args, **new)

    def _get_map(self):
        """Can be implemented by subclasses to support str -> Enum conversion.

        To get data from all subclasses, we always fetch _get_map from super(),
        append our own shit and return it.
        """
        return {}

    def __pretty__(
        self, fmt: Callable[[Any], Any], **kwargs: Any
    ) -> Generator[Any, None, None]:
        yield f"{type(self).__name__}("
        yield 1
        for k, v in self.get_properties(only_writable=True).items():
            yield f"{k}={v!r}"
            yield 0
            for ef in self._eventfilters:
                yield f"Eventfilter={ef.__class__.__name__}"
                yield 0
        yield -1
        yield ")"

    # def __repr__(self):  # we already monkeypatch QObject
    #     return get_repr(self, self.objectName())

    def __setstate__(self, state):
        self.set_properties(state)

    def __getstate__(self):
        return self.get_properties()

    def __reduce__(self):
        return type(self), (), self.__getstate__()

    def __getattr__(self, val):
        cameled = helpers.to_lower_camel(val)
        if cameled in dir(self):
            return getattr(self, cameled)
        raise AttributeError(val)

    def installEventFilter(self, filter_: QtCore.QObject | str, **kwargs):
        """Override to also allow setting eventfilters by name."""
        if filter_ in self._eventfilters:
            logger.warning("Trying to install same EventFilter multiple times.")
            return
        match filter_:
            case QtCore.QObject():
                pass
            case str():
                from prettyqt import eventfilters

                Klass = helpers.get_class_for_id(eventfilters.BaseEventFilter, filter_)
                filter_ = Klass(parent=self, **kwargs)
            case _:
                raise ValueError(filter_)
        self._eventfilters.add(filter_)
        super().installEventFilter(filter_)

    def removeEventFilter(self, eventfilter: QtCore.QObject):
        if eventfilter not in self._eventfilters:
            logger.warning("Trying to remove non-installed EventFilter.")
            return
        self._eventfilters.remove(eventfilter)
        super().removeEventFilter(eventfilter)

    def add_callback_for_event(
        self,
        callback: Callable[[QtCore.QEvent], bool],
        include: QtCore.QEvent.Type | Sequence[QtCore.QEvent.Type] | None = None,
        exclude: QtCore.QEvent.Type | Sequence[QtCore.QEvent.Type] | None = None,
    ) -> eventfilters.EventCatcher:
        """Connect widget events to a callback.

        if include is set, it behaves like a whitelist.
        if exclude is set, it behaves like a blacklist.
        The QEvent is passed to the callback as an argument, and the callback
        needs to return True or False to indicate whether the Event should be filtered.

        Arguments:
            callback: Callback to execute when event is triggered
            include: Events to include
            exclude: Events to exclude
        """
        from prettyqt import eventfilters

        eventfilter = eventfilters.EventCatcher(include, exclude, callback, parent=self)
        self.installEventFilter(eventfilter)
        return eventfilter

    def serialize(self) -> dict[str, Any]:
        return self.get_properties()
        # dct = {}
        # for klass in reversed(inspect.getmro(type(self))):
        #     if "serialize_fields" in klass.__dict__:
        #         data = klass.serialize_fields(self)  # type: ignore
        #         dct |= data
        # return dct

    @contextlib.contextmanager
    def block_signals(self):
        """Context manager to temporarily block emitting signals."""
        blocked = self.blockSignals(True)
        yield None
        self.blockSignals(blocked)

    def to_json(self):
        dct = self.__getstate__()
        for k, v in dct.items():
            if isinstance(v, ObjectMixin):
                dct[k] = v.to_json()
        return dct

    def set_unique_id(self):
        """Set unique objectName."""
        class_name = type(self).__name__
        count = next(counter_dict[class_name])
        self.set_id(f"{class_name}_{count}")

    def set_id(self, name: str):
        self.setObjectName(name)

    def get_id(self) -> str:
        return self.objectName()

    def has_id(self) -> bool:
        return self.objectName() != ""

    @classmethod
    def get_static_metaobject(cls) -> core.MetaObject:
        return core.MetaObject(cls.staticMetaObject)

    def get_metaobject(self) -> core.MetaObject:
        return core.MetaObject(self.metaObject())

    # @property
    # def id(self) -> str:
    #     return self.objectName()

    # @id.setter
    # def id(self, name: str):
    #     self.setObjectName(name)

    def find_children(
        self,
        typ: type[T] = QtCore.QObject,
        name: str | datatypes.PatternType | None = None,
        recursive: bool = True,
        property_selector: dict[str, datatypes.VariantType | Callable] | None = None,
        only_prettyqt_classes: bool = False,
    ) -> listdelegators.BaseListDelegator[T]:
        """Find children with given type and name.

        Children can be filtered by passing a property selector dictionary.
        It must contain the property name for keys and either a value which must be set
        or a predicate function which gets the property value as an argument
        and must return True if the child should be included.

        Arguments:
            typ: Subclass of QObject (can also be a UnionType)
            name: ObjectName filter. None includes all.
            recursive: whether to search for children recursively.
            property_selector: dict containing PropertyName -> Value/Predicate pairs.
            only_prettyqt_classes: only include objects with prettyqt superpowers.

        Returns:
            list of QObjects
        """
        if isinstance(name, re.Pattern):
            name = core.RegularExpression(name)
        if recursive:
            flag = QtCore.Qt.FindChildOption.FindChildrenRecursively
        else:
            flag = QtCore.Qt.FindChildOption.FindDirectChildrenOnly
        match typ:
            case types.UnionType():
                objects = [
                    i
                    for t in get_args(typ)
                    for i in self.findChildren(t, name=name, options=flag)
                ]
            case type():
                objects = self.findChildren(typ, name=name, options=flag)
            case _:
                raise TypeError(typ)
        if property_selector:
            objects = [
                o
                for o in objects
                for k, v in property_selector.items()
                if (callable(v) and v(o.property(k)))
                or (not callable(v) and o.property(k) == v)
            ]
        if only_prettyqt_classes:
            objects = [i for i in objects if i.__module__.startswith("prettyqt")]
        return listdelegators.BaseListDelegator(objects)

    def find_child(
        self,
        typ: type[T] = QtCore.QObject,
        name: str | QtCore.QRegularExpression | None = None,
        recursive: bool = True,
    ) -> T | None:
        """Find a child with given type and name."""
        if recursive:
            flag = QtCore.Qt.FindChildOption.FindChildrenRecursively
        else:
            flag = QtCore.Qt.FindChildOption.FindDirectChildrenOnly
        return self.findChild(typ, name, flag)  # type: ignore

    def find_parent(
        self, typ: type[T] = QtCore.QObject, name: str | None = None
    ) -> T | None:
        """Find parent with given type or name."""
        node = self
        while node:
            node = node.parent()
            if isinstance(node, typ) and (name is None or node.objectName() == name):
                return node
        return None

    def start_timer(
        self,
        interval: int | str,
        timer_type: constants.TimerTypeStr = "coarse",
    ) -> int | None:
        """Start a timer and return the timer id, to be used in timerEvent."""
        if isinstance(interval, str):
            interval = helpers.parse_time(interval)
        result = self.startTimer(interval, constants.TIMER_TYPE[timer_type])
        return None if result == 0 else result

    def start_callback_timer(
        self,
        callback: Callable,
        interval: int | str,
        single_shot: bool = False,
        timer_type: constants.TimerTypeStr = "coarse",
    ) -> core.Timer:
        """Start timer and execute callback when timeout reached."""
        interval = helpers.parse_time(interval) if isinstance(interval, str) else interval
        timer = core.Timer(
            self,
            single_shot=single_shot,
            interval=interval,
            timer_type=timer_type,
            timeout=callback,
        )
        timer.start()
        return timer

    def get_properties(
        self,
        include_super: bool = True,
        cast: bool = True,
        only_writable: bool = False,
        only_nonempty: bool = False,
    ) -> dict[str, Any]:
        """Get a dictionary containing all properties and their values."""
        metaobj = self.get_metaobject()
        props = metaobj.get_properties(
            include_super=include_super, only_writable=only_writable
        )
        dct = {}
        for i in props:
            if i.get_name() in ["children", "frameShadow", "state"]:
                continue
            val = i.read(self)
            if only_nonempty:
                match val:
                    case _ if hasattr(val, "isNull"):
                        include = not val.isNull()
                    case _ if hasattr(val, "isEmpty"):
                        include = val.isEmpty()
                    case _ if hasattr(val, "isValid"):
                        include = val.isValid()
                    case _:
                        include = bool(val)
            else:
                include = True
            if not include:
                continue
            dct[i.name()] = datatypes.make_serializable(val) if cast else val
        return dct

    def set_properties(self, props: dict[str, Any], include_super: bool = True):
        """Set properties from a dictionary."""
        metaobj = self.get_metaobject()
        metaprops = metaobj.get_properties(include_super=include_super)
        for metaprop in metaprops:
            if (name := metaprop.name()) in props:
                value = props[name]
                metaprop.write(self, value)

    def get_dynamic_properties(self) -> dict[str, Any]:
        """Get a dictionary with all dynamic properties."""
        return {
            (k := i.data().decode()): self.property(k)
            for i in self.dynamicPropertyNames()
        }


class Object(ObjectMixin, QtCore.QObject):
    pass


if __name__ == "__main__":
    from prettyqt import widgets

    app = widgets.app()
    obj = core.Object(object_name="jkjk")
    test = widgets.TableWidget()
    meta = obj.get_metaobject()
    prop = meta.get_property(0)
    with app.debug_mode():
        app.sleep(1)
