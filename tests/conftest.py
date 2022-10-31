"""Tests for `datacook` package."""
from __future__ import annotations

import pytest

from prettyqt import gui, widgets
from prettyqt.qt import QtCore, QtWidgets


# import pytest


@pytest.fixture
def tablewidget():
    widget = widgets.TableWidget()
    widget.setColumnCount(3)
    widget.insertRow(0)
    widget.setHorizontalHeaderLabels(["LIB", "CELL", "area"])
    item = widgets.TableWidgetItem("test")
    widget.setItem(0, 0, item)
    widget.setItem(1, 1, widgets.TableWidgetItem("test"))
    return widget


@pytest.fixture(scope="session")
def qapp_cls():
    return widgets.Application


class QtTester:
    @staticmethod
    def send_keypress(widget: QtWidgets.QWidget, key):
        event = gui.KeyEvent(
            QtCore.QEvent.Type.KeyPress,
            key,
            QtCore.Qt.KeyboardModifier(0),  # type: ignore
        )
        widgets.Application.sendEvent(widget, event)

    @staticmethod
    def send_mousepress(widget: QtWidgets.QWidget, key):
        event = gui.MouseEvent(  # type: ignore
            QtCore.QEvent.Type.MouseButtonRelease,
            QtCore.QPointF(0, 0),
            QtCore.QPointF(0, 0),
            key,
            QtCore.Qt.MouseButton.NoButton,
            QtCore.Qt.KeyboardModifier(0),  # type: ignore
        )
        widgets.Application.sendEvent(widget, event)

    @staticmethod
    def send_mousemove(
        widget: QtWidgets.QWidget, target: QtCore.QPointF | None = None, delay: int = 0
    ):
        if target is None:
            target = QtCore.QPointF(0, 0)
        event = gui.MouseEvent(  # type: ignore
            QtCore.QEvent.Type.MouseButtonRelease,
            target,
            QtCore.QPointF(0, 0),
            QtCore.Qt.MouseButton.NoButton,
            QtCore.Qt.MouseButton.NoButton,
            QtCore.Qt.KeyboardModifier(0),  # type: ignore
        )
        widgets.Application.sendEvent(widget, event)

    # @staticmethod
    # def test_model(model: QtCore.QAbstractItemModel, force_py: bool = False):
    #     tester = modeltest.ModelTester(model)
    #     tester.check(force_py=force_py)
    #     tester._cleanup()


@pytest.fixture
def qttester() -> type[QtTester]:
    return QtTester
