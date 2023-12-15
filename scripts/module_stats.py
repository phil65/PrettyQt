from __future__ import annotations

import importlib
import pkgutil
import types

import PyQt6
import PySide6

import prettyqt
from prettyqt import core, gui, widgets
from prettyqt.qt import QtCore, QtGui, QtWidgets


OBSELETE = ["QPictureIO", "QDesktopWidget", "QDirModel"]

mapper = {gui: QtGui, widgets: QtWidgets, core: QtCore}

if __name__ == "__main__":
    for k, v in mapper.items():
        theirs = dir(v)
        ours = dir(k)
        print(f"Missing modules for {k.__name__}")
        for i in theirs:
            if i[1:] not in ours and i[0] == "Q" and i not in OBSELETE:
                print(f"{v.__name__}.{i}")


class API:
    def __init__(self, module: types.ModuleType):
        self.module = module
        self._api = module.__name__

    def qt_name(self, name):
        return name

    def list_modules(self, force_qt_naming=False):
        return [p.name for p in pkgutil.iter_modules(self.module.__path__)]

    def import_modules(self):
        return [importlib.import_module(p) for p in self.list_modules()]

    def compare_with(self, other: API):
        theirs = dir(other.module)
        ours = dir(self.module)
        print(f"Missing modules for {self.module.__name__}")

        for i in theirs:
            if i not in ours and i not in OBSELETE:
                print(f"{v.__name__}.{i}")


class PrettyQtApi(API):
    MODULE = prettyqt

    def compare_with(self, other: API):
        theirs = dir(other.module)
        ours = dir(self.module)
        print(f"Missing modules for {self.module.__name__}")

        for i in theirs:
            if i[1:] not in ours and i[0] == "Q" and i not in OBSELETE:
                print(f"{v.__name__}.{i}")


class PySide6Api(API):
    MODULE = PyQt6


class PyQt6Api(API):
    MODULE = PySide6
