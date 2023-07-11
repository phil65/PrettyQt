"""test module.

contains QtTest-based classes
"""

from .abstractitemmodeltester import AbstractItemModelTester
from .signalspy import SignalSpy
from prettyqt.qt import QtTest

QT_MODULE = QtTest

__all__ = ["SignalSpy", "AbstractItemModelTester"]
