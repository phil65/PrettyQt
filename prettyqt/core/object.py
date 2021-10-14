from __future__ import annotations

from collections import defaultdict
import contextlib
import inspect
import itertools
from typing import Any, DefaultDict, TypeVar

from prettyqt import constants, core
import prettyqt.qt
from prettyqt.qt import QtCore
from prettyqt.utils import helpers


T = TypeVar("T", bound=QtCore.QObject)

counter_dict: DefaultDict = defaultdict(itertools.count)


class Object(QtCore.QObject):
    def __repr__(self):
        return f"{type(self).__name__}()"

    def __setstate__(self, state):
        self.set_id(state["object_name"])

    def __getstate__(self):
        return self.serialize()

    def __reduce__(self):
        return type(self), (), self.__getstate__()

    def serialize_fields(self):
        return dict(object_name=self.objectName())

    def serialize(self) -> dict[str, Any]:
        dct = {}
        for klass in reversed(inspect.getmro(type(self))):
            if "serialize_fields" in klass.__dict__:
                data = klass.serialize_fields(self)  # type: ignore
                dct.update(data)
        return dct

    @contextlib.contextmanager
    def block_signals(self):
        blocked = self.blockSignals(True)
        yield None
        self.blockSignals(blocked)

    def to_json(self):
        dct = self.__getstate__()
        for k, v in dct.items():
            if isinstance(v, QtCore.QObject):
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
    def get_metaobject(cls) -> core.MetaObject:
        return core.MetaObject(cls.staticMetaObject)

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
        if prettyqt.qt.API != "pyside2":
            return self.findChildren(typ, name=name, options=flag)  # type: ignore
        else:
            if name is None:
                items = self.findChildren(typ)
            else:
                items = self.findChildren(typ, name)
            return [i for i in items if recursive or i.parent() == self]

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
        if prettyqt.qt.API != "pyside2":
            return self.findChild(typ, name, flag)  # type: ignore
        else:
            if name is None:
                item = self.findChild(typ)
            else:
                item = self.findChild(typ, name)
            return item if recursive or item.parent() == self else None  # type: ignore

    def find_parent(
        self, typ: type[QtCore.QObject], name: str | None = None
    ) -> QtCore.QObject | None:
        node = self
        while node:
            node = node.parent()
            if isinstance(node, typ):
                if name is None or node.objectName() == name:
                    return node
        return None

    def start_timer(
        self, interval: int | str, timer_type: constants.TimerTypeStr = "coarse"
    ) -> int:
        if isinstance(interval, str):
            interval = helpers.parse_time(interval)
        return self.startTimer(interval, constants.TIMER_TYPE[timer_type])
