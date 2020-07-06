# -*- coding: utf-8 -*-
"""
"""

from contextlib import contextmanager
import itertools
import collections

from qtpy import QtCore

counter_dict = collections.defaultdict(itertools.count)


class Object(QtCore.QObject):

    def __getstate__(self):
        return dict(object_name=self.objectName())

    def __setstate__(self, state):
        self.__init__()
        self.set_id(state["object_name"])

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

    def get_id(self):
        return self.objectName()

    @property
    def id(self) -> str:
        return self.objectName()

    @id.setter
    def id(self, name: str):
        self.setObjectName(name)

    def find_children(self, typ, recursive: bool = True):
        if recursive:
            flag = QtCore.Qt.FindChildrenRecursively
        else:
            flag = QtCore.Qt.FindDirectChildrenOnly
        return self.findChildren(typ, options=flag)
