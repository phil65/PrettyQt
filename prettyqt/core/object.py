from __future__ import annotations

from collections import defaultdict
import contextlib

# import inspect
import itertools
from typing import Any, TypeVar

from prettyqt import constants, core
from prettyqt.qt import QtCore
from prettyqt.utils import datatypes, helpers


T = TypeVar("T", bound=QtCore.QObject)

counter_dict: defaultdict = defaultdict(itertools.count)


class ObjectMixin:
    Properties: dict[type, list[str]] = {}

    def __init__(self, *args, **kwargs):
        # this allows snake_case property and signal names in ctor.
        new = {}
        if kwargs:
            mapper = self._get_map()
            for k, v in kwargs.items():
                if (camel_k := helpers.to_lower_camel(k)) in mapper and isinstance(
                    v, str
                ):
                    new[camel_k] = mapper[camel_k][v]
                elif k in {"window_icon", "icon"} and isinstance(v, str):
                    from prettyqt import iconprovider

                    new[camel_k] = iconprovider.get_icon(v)
                else:
                    new[camel_k] = v
        super().__init__(*args, **new)

    def _get_map(self):
        """Can be implemented by subclasses to support str -> Enum conversion.

        To get data from all subclasses, we always fetch _get_map from super(),
        append our own shit and return it.
        """
        return {}

    def __repr__(self):
        return f"{type(self).__name__}()"

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
        self, interval: int | str, timer_type: constants.TimerTypeStr = "coarse"
    ) -> int | None:
        if isinstance(interval, str):
            interval = helpers.parse_time(interval)
        result = self.startTimer(interval, constants.TIMER_TYPE[timer_type])
        return None if result == 0 else result

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
            i.data().decode(): self.property(i.data().decode())
            for i in self.dynamicPropertyNames()
        }


class Object(ObjectMixin, QtCore.QObject):
    pass


if __name__ == "__main__":
    import logging
    import pickle
    import sys

    from prettyqt import widgets

    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
    app = widgets.app()
    obj = core.Object(object_name="jkjk")
    meta = obj.get_metaobject()
    prop = meta.get_property(0)
    print(obj.get_properties())
    with open("data.pkl", "wb") as jar:
        pickle.dump(obj, jar)
    with open("data.pkl", "rb") as jar:
        obj = pickle.load(jar)
