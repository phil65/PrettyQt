from collections import defaultdict
from contextlib import contextmanager
import inspect
import itertools
from typing import DefaultDict, List, Optional, Type, Union

import qtpy
from qtpy import QtCore


counter_dict: DefaultDict = defaultdict(itertools.count)


class Object(QtCore.QObject):
    def __repr__(self):
        return f"{self.__class__.__name__}()"

    def __setstate__(self, state):
        self.set_id(state["object_name"])

    def __getstate__(self):
        return self.serialize()

    def __reduce__(self):
        return type(self), (), self.__getstate__()

    def serialize_fields(self):
        return dict(object_name=self.objectName())

    def serialize(self):
        dct = dict()
        for klass in reversed(inspect.getmro(type(self))):
            if "serialize_fields" in klass.__dict__:
                data = klass.serialize_fields(self)  # type: ignore
                dct.update(data)
        return dct

    @contextmanager
    def block_signals(self):
        self.blockSignals(True)
        yield None
        self.blockSignals(False)

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

    # @property
    # def id(self) -> str:
    #     return self.objectName()

    # @id.setter
    # def id(self, name: str):
    #     self.setObjectName(name)

    def find_children(
        self,
        typ: Type[QtCore.QObject] = QtCore.QObject,
        name: Optional[Union[str, QtCore.QRegularExpression]] = None,
        recursive: bool = True,
    ) -> List[QtCore.QObject]:
        if recursive:
            flag = QtCore.Qt.FindChildrenRecursively
        else:
            flag = QtCore.Qt.FindDirectChildrenOnly
        if qtpy.API == "pyqt5":
            return self.findChildren(typ, name=name, options=flag)
        else:
            return [
                i for i in self.findChildren(typ, name) if recursive or i.parent() == self
            ]

    def find_child(
        self,
        typ: Type[QtCore.QObject] = QtCore.QObject,
        name: Optional[Union[str, QtCore.QRegularExpression]] = None,
        recursive: bool = True,
    ) -> Optional[QtCore.QObject]:
        if recursive:
            flag = QtCore.Qt.FindChildrenRecursively
        else:
            flag = QtCore.Qt.FindDirectChildrenOnly
        if qtpy.API == "pyqt5":
            return self.findChild(typ, name=name, options=flag)
        else:
            item = self.findChild(typ, name)
            return item if recursive or item.parent() == self else None

    def find_parent(
        self, typ: Type[QtCore.QObject], name: Optional[str] = None
    ) -> Optional[QtCore.QObject]:
        node = self
        while node:
            node = node.parent()
            if isinstance(node, typ):
                if name is None or node.objectName() == name:
                    return node
        return None
