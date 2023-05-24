from __future__ import annotations

from collections import defaultdict
from collections.abc import Callable, Container
import contextlib

# import inspect
import itertools
import logging
from typing import TYPE_CHECKING, Any, TypeVar

from typing_extensions import Self

from prettyqt import constants, core
from prettyqt.qt import QtCore
from prettyqt.utils import datatypes, get_repr, helpers


if TYPE_CHECKING:
    from prettyqt import eventfilters

T = TypeVar("T", bound=QtCore.QObject)

counter_dict: defaultdict = defaultdict(itertools.count)

logger = logging.getLogger(__name__)


class ObjectMixin:
    Properties: dict[type, list[str]] = {}

    def __init__(self, *args, **kwargs):
        self._eventfilters = set()
        new = {}
        if kwargs:
            mapper = self._get_map()
            for k, v in kwargs.items():
                # this allows snake_case naming.
                camel_k = helpers.to_lower_camel(k)
                # allow str values instead of enum
                if camel_k in mapper and isinstance(v, str):
                    new[camel_k] = mapper[camel_k][v]
                # allow str values for common icon kwargs
                elif k in {"window_icon", "icon"} and isinstance(v, str):
                    from prettyqt import iconprovider

                    new[camel_k] = iconprovider.get_icon(v)
                # regular case
                else:
                    new[camel_k] = v
        super().__init__(*args, **new)

    def _get_map(self):
        """Can be implemented by subclasses to support str -> Enum conversion.

        To get data from all subclasses, we always fetch _get_map from super(),
        append our own shit and return it.
        """
        return {}

    def __repr__(self):  # we already monkeypatch QObject
        return get_repr(self, self.objectName())

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

    def installEventFilter(self, eventfilter: QtCore.QObject):
        if eventfilter in self._eventfilters:
            logger.warning("Trying to install same EventFilter multiple times.")
            return
        self._eventfilters.add(eventfilter)
        super().installEventFilter(eventfilter)

    def removeEventFilter(self, eventfilter: QtCore.QObject):
        if eventfilter not in self._eventfilters:
            logger.warning("Trying to remove non-installed EventFilter.")
            return
        self._eventfilters.remove(eventfilter)
        super().removeEventFilter(eventfilter)

    def add_callback_for_event(
        self,
        callback: Callable[[QtCore.QEvent], bool],
        include: QtCore.QEvent.Type | Container[QtCore.QEvent.Type] | None = None,
        exclude: QtCore.QEvent.Type | Container[QtCore.QEvent.Type] | None = None,
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

    def serialize_fields(self):
        return dict(object_name=self.objectName())

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
        name: str | QtCore.QRegularExpression | None = None,
        recursive: bool = True,
    ) -> list[T]:
        if recursive:
            flag = QtCore.Qt.FindChildOption.FindChildrenRecursively
        else:
            flag = QtCore.Qt.FindChildOption.FindDirectChildrenOnly
        return self.findChildren(typ, name=name, options=flag)  # type: ignore

    def find_child(
        self,
        typ: type[T] = QtCore.QObject,
        name: str | QtCore.QRegularExpression | None = None,
        recursive: bool = True,
    ) -> T | None:
        if recursive:
            flag = QtCore.Qt.FindChildOption.FindChildrenRecursively
        else:
            flag = QtCore.Qt.FindChildOption.FindDirectChildrenOnly
        return self.findChild(typ, name, flag)  # type: ignore

    def find_parent(
        self, typ: type[T] = QtCore.QObject, name: str | None = None
    ) -> T | None:
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
    ) -> int | None:
        if isinstance(interval, str):
            interval = helpers.parse_time(interval)
        timer = core.Timer(
            self, single_shot=single_shot, interval=interval, timer_type=timer_type
        )
        timer.timeout.connect(callback)
        timer.start()
        return timer

    def get_properties(
        self, include_super: bool = True, cast: bool = True
    ) -> dict[str, Any]:
        metaobj = self.get_metaobject()
        props = metaobj.get_properties(include_super=include_super)
        return {
            i.name(): datatypes.make_serializable(i.read(self))
            for i in props
            if i.get_name() not in ["children", "frameShadow", "state"]
        }

    def set_properties(self, props: dict[str, Any], include_super: bool = True):
        metaobj = self.get_metaobject()
        metaprops = metaobj.get_properties(include_super=include_super)
        for metaprop in metaprops:
            if (name := metaprop.name()) in props:
                value = props[name]
                metaprop.write(self, value)

    def get_dynamic_properties(self) -> dict[str, Any]:
        return {
            (k := i.data().decode()): self.property(k)
            for i in self.dynamicPropertyNames()
        }

    def copy(self) -> Self:
        metaobj = self.get_metaobject()
        new = type(self)()
        for prop in metaobj.get_properties(only_writable=True):
            val = prop.read(self)
            prop.write(new, val)
        # MetaObject can return non-existing signals, dont know why.
        # also filter out duplicates.
        signal_names = {
            s.get_name() for s in metaobj.get_signals() if hasattr(self, s.get_name())
        }
        for signal_name in signal_names:
            own_signal = self.__getattribute__(signal_name)
            new_signal = new.__getattribute__(signal_name)
            # own_signal.connect(new_signal)
            new_signal.connect(own_signal)
            logger.debug(f"connected {signal_name}")
        return new


class Object(ObjectMixin, QtCore.QObject):
    pass


if __name__ == "__main__":
    from prettyqt import widgets

    app = widgets.app()
    obj = core.Object(object_name="jkjk")
    obj.copy()
    meta = obj.get_metaobject()
    prop = meta.get_property(0)
    with app.debug_mode():
        app.sleep(1)
