# -*- coding: utf-8 -*-

from typing import Optional, Union, DefaultDict, List
from collections import defaultdict
from contextlib import contextmanager
import itertools

from qtpy import QtCore, QtWidgets

from prettyqt import core

counter_dict: DefaultDict = defaultdict(itertools.count)


class Object(QtCore.QObject):
    def serialize_fields(self):
        return dict(object_name=self.objectName())

    def __setstate__(self, state):
        self.__init__()
        self.set_id(state["object_name"])

    def __getstate__(self):
        return self.serialize()

    def serialize(self):
        classes = type(self).mro()
        dct = dict()
        for klass in reversed(classes):
            if "serialize_fields" in klass.__dict__:
                data = klass.serialize_fields(self)
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

    @property
    def id(self) -> str:
        return self.objectName()

    @id.setter
    def id(self, name: str):
        self.setObjectName(name)

    def find_children(
        self,
        typ=QtCore.QObject,
        name: Optional[Union[str, QtCore.QRegularExpression]] = None,
        recursive: bool = True,
    ) -> List[QtCore.QObject]:
        if recursive:
            flag = QtCore.Qt.FindChildrenRecursively
        else:
            flag = QtCore.Qt.FindDirectChildrenOnly
        return self.findChildren(typ, name=name, options=flag)

    def find_child(
        self,
        typ=QtCore.QObject,
        name: Optional[Union[str, QtCore.QRegularExpression]] = None,
        recursive: bool = True,
    ):
        if recursive:
            flag = QtCore.Qt.FindChildrenRecursively
        else:
            flag = QtCore.Qt.FindDirectChildrenOnly
        return self.findChild(typ, name, options=flag)

    def store_widget_states(self, settings=None, key: str = "states"):
        splitters = self.find_children(QtWidgets.QSplitter)
        splitter_dct = {
            sp.objectName(): sp.saveState() for sp in splitters if sp.objectName()
        }
        mainwindows = self.find_children(QtWidgets.QMainWindow)
        mw_dct = {
            mw.objectName(): mw.saveState() for mw in mainwindows if mw.objectName()
        }
        headerviews = self.find_children(QtWidgets.QHeaderView)
        headerview_dct = {
            h.objectName(): h.saveState() for h in headerviews if h.objectName()
        }
        settings = core.Settings() if settings is None else settings
        settings[key] = dict(
            splitters=splitter_dct, mainwindows=mw_dct, headerviews=headerview_dct
        )

    def restore_widget_states(self, settings=None, key: str = "states"):
        settings = core.Settings() if settings is None else settings
        splitters = settings[key].get("splitters")
        mainwindows = settings[key].get("splitters")
        headerviews = settings[key].get("headerviews")
        if splitters is not None:
            for k, v in splitters.items():
                w = self.find_child(QtWidgets.QSplitter, name=k)
                if w is not None:
                    w.restoreState(v)
        if mainwindows is not None:
            for k, v in mainwindows.items():
                w = self.find_child(QtWidgets.QMainWindow, name=k)
                if w is not None:
                    w.restoreState(v)
        if headerviews is not None:
            for k, v in headerviews.items():
                w = self.find_child(QtWidgets.QHeaderView, name=k)
                if w is not None:
                    w.restoreState(v)

    def find_parent(
        self, typ: QtCore.QObject, name: Optional[str] = None
    ) -> Optional[QtCore.QObject]:
        node = self
        while node:
            node = node.parent()
            if isinstance(node, typ):
                if name is None or node.objectName() == name:
                    return node
        return None

    def raise_dock(self) -> bool:
        w = self.find_parent(QtWidgets.QDockWidget)
        if w is None:
            return False
        w.setVisible(True)
        w.raise_()
        return True
