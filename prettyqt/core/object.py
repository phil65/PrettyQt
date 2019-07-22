# -*- coding: utf-8 -*-
"""
@author: Philipp Temminghoff
"""

from contextlib import contextmanager

from qtpy import QtCore


class Object(QtCore.QObject):

    def __getstate__(self):
        return dict(object_name=self.objectName())

    def __setstate__(self, state):
        self.__init__()
        self.id = state["object_name"]

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

    def set_object_name(self, name: str):
        self.setObjectName(name)

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
