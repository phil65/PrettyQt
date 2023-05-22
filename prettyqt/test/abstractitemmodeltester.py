from __future__ import annotations

from prettyqt import core
from prettyqt.qt import QtTest


class AbstractItemModelTester(core.ObjectMixin, QtTest.QAbstractItemModelTester):
    pass


if __name__ == "__main__":
    from prettyqt import gui

    model = gui.StandardItemModel()
    tester = AbstractItemModelTester(model)
