from __future__ import annotations

from collections import defaultdict
from collections.abc import Callable, Generator, Sequence
import contextlib

# import inspect
import itertools
import logging
import re
import types

from typing import TYPE_CHECKING, Any, TypeVar, get_args

from prettyqt import constants, core
from prettyqt.utils import classhelpers, datatypes, helpers, listdelegators


if TYPE_CHECKING:
    from prettyqt import eventfilters

T = TypeVar("T", bound=core.QObject)

counter_dict: defaultdict = defaultdict(itertools.count)

logger = logging.getLogger(__name__)

_properties = {}
_signals = {}


def get_properties(klass):
    if klass not in _properties:
        metaobj = core.MetaObject(klass.staticMetaObject)
        _properties[klass] = [i.get_name() for i in metaobj.get_properties()]
    return _properties[klass]


def get_signals(klass):
    if klass not in _signals:
        metaobj = core.MetaObject(klass.staticMetaObject)
        _signals[klass] = [i.get_name() for i in metaobj.get_signals()]
    return _signals[klass]


class ObjectMixin:
    def __init__(self, *args, **kwargs):
        self._eventfilters = set()
        # klass = type(self)
        # if issubclass(klass, core.QObject) and klass not in _properties:
        #     metaobj = core.MetaObject(klass.staticMetaObject)
        #     _properties[klass] = [i.get_name() for i in metaobj.get_properties()]
        #     _signals[klass] = [i.get_name() for i in metaobj.get_signals()]
        new = {}
        if kwargs:
            mapper = self._get_map()
            props = get_properties(type(self))
            signals = get_signals(type(self))
            for k, v in kwargs.items():
                # this allows snake_case naming.
                camel_k = helpers.to_lower_camel(k)
                if camel_k != k and camel_k in kwargs:
                    logger.warning(f"{k} defined twice: {v} / {kwargs[camel_k]}")
                # allow str values instead of enum
                if camel_k in mapper and isinstance(v, str):
                    new[camel_k] = mapper[camel_k][v]
                # allow str values for common icon kwargs
                elif camel_k in {"windowIcon", "icon"} and isinstance(v, str):
                    from prettyqt import iconprovider

                    new[camel_k] = iconprovider.get_icon(v)
                # kwargs which need camel-casing
                elif camel_k in props or camel_k in signals:
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

    def installEventFilter(self, filter_: core.QObject | str, **kwargs):
        """Override to also allow setting eventfilters by name."""
        if filter_ in self._eventfilters:
            logger.warning(f"Installing same EventFilter multiple times to {self}.")
            return
        match filter_:
            case core.QObject():
                pass
            case str():
                from prettyqt import eventfilters

                Klass = classhelpers.get_class_for_id(
                    eventfilters.BaseEventFilter, filter_
                )
                filter_ = Klass(parent=self, **kwargs)
            case _:
                raise ValueError(filter_)
        self._eventfilters.add(filter_)
        super().installEventFilter(filter_)

    def removeEventFilter(self, eventfilter: core.QObject):
        if eventfilter not in self._eventfilters:
            logger.warning("Trying to remove non-installed EventFilter.")
            return
        self._eventfilters.remove(eventfilter)
        super().removeEventFilter(eventfilter)

    def add_callback_for_event(
        self,
        callback: Callable[[core.QEvent], bool],
        include: core.QEvent.Type | Sequence[core.QEvent.Type] | None = None,
        exclude: core.QEvent.Type | Sequence[core.QEvent.Type] | None = None,
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
    def signals_blocked(self):
        """Context manager to temporarily block emitting signals."""
        blocked = self.blockSignals(True)
        yield self
        self.blockSignals(blocked)

    @contextlib.contextmanager
    def signal_blocked(
        self, signal: core.SignalInstance, receiver: Callable | core.SignalInstance
    ):
        """Context manager to temporarily disconnect specific signal."""
        signal.disconnect(receiver)
        yield self
        signal.connect(receiver)

    @contextlib.contextmanager
    def properties_set_to(self, **kwargs):
        """Context manager to temporarily set properties to different values."""
        props = {k: self.property(k) for k in kwargs}
        for k, v in kwargs.items():
            self.setProperty(k, v)
        yield self
        for k, v in props.items():
            self.setProperty(k, v)

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
        self.setObjectName(f"{class_name}_{count}")

    @classmethod
    def get_static_metaobject(cls) -> core.MetaObject:
        return core.MetaObject(cls.staticMetaObject)

    def get_metaobject(self) -> core.MetaObject:
        return core.MetaObject(self.metaObject())

    def find_children(
        self,
        typ: type[T] = core.QObject,
        name: str | datatypes.PatternType | None = None,
        recursive: bool = True,
        property_selector: dict[str, datatypes.VariantType | Callable] | None = None,
        only_prettyqt_classes: bool = False,
    ) -> listdelegators.ListDelegator[T]:
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
            flag = constants.FindChildOption.FindChildrenRecursively
        else:
            flag = constants.FindChildOption.FindDirectChildrenOnly
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
        return listdelegators.ListDelegator(objects)

    def find_child(
        self,
        typ: type[T] = core.QObject,
        name: str | core.QRegularExpression | None = None,
        recursive: bool = True,
    ) -> T | None:
        """Find a child with given type and name."""
        if recursive:
            flag = constants.FindChildOption.FindChildrenRecursively
        else:
            flag = constants.FindChildOption.FindDirectChildrenOnly
        match typ:
            case types.UnionType():
                return next(
                    (item for item in self.find_children(typ, name, recursive=recursive)),
                    None,
                )

            case _:
                return self.findChild(typ, name, flag)  # type: ignore

    def find_parent(
        self, typ: type[T] = core.QObject, name: str | None = None
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
                        include = not val.isEmpty()
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

    def bind_property(cls, object_name: str, prop_name: str) -> property:
        def getter(self):
            return self.findChild(cls, object_name).property(prop_name)

        def setter(self, value):
            self.findChild(cls, object_name).setProperty(prop_name, value)

        return property(getter, setter)


class Object(ObjectMixin, core.QObject):
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
