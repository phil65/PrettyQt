#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `datacook` package."""

# import pytest

import pytest
from qtpy import QtCore
from prettyqt import widgets, gui
from prettyqt.utils import modeltest


@pytest.fixture(scope="session")
def qapp():
    app = widgets.Application([])
    app.set_metadata(
        app_name="test", app_version="1.0.0", org_name="test", org_domain="test"
    )
    yield app


@pytest.fixture
def tablewidget():
    widget = widgets.TableWidget()
    widget.setColumnCount(3)
    widget.insertRow(0)
    widget.setHorizontalHeaderLabels(["LIB", "CELL", "area"])
    item = widgets.TableWidgetItem("test")
    widget.setItem(0, 0, item)
    return widget
    widget.setItem(1, 1, widgets.TableWidgetItem("test"))


class QtTester:
    @staticmethod
    def send_keypress(widget, key):
        event = gui.KeyEvent(QtCore.QEvent.KeyPress, key, QtCore.Qt.KeyboardModifiers(0))
        widgets.Application.sendEvent(widget, event)

    @staticmethod
    def send_mousepress(widget, key):
        event = gui.MouseEvent(
            QtCore.QEvent.MouseButtonRelease,
            QtCore.QPointF(0, 0),
            QtCore.QPointF(0, 0),
            key,
            QtCore.Qt.NoButton,
            QtCore.Qt.KeyboardModifiers(0),
        )
        widgets.Application.sendEvent(widget, event)

    @staticmethod
    def send_mousemove(widget, target=None, delay=0):
        if target is None:
            target = QtCore.QPointF(0, 0)
        event = gui.MouseEvent(
            QtCore.QEvent.MouseButtonRelease,
            target,
            QtCore.QPointF(0, 0),
            QtCore.Qt.NoButton,
            QtCore.Qt.NoButton,
            QtCore.Qt.KeyboardModifiers(0),
        )
        widgets.Application.sendEvent(widget, event)

    @staticmethod
    def test_model(model, force_py):
        tester = modeltest.ModelTester()
        tester.check(model, force_py=force_py)
        tester._cleanup()


@pytest.fixture
def qttester():
    return QtTester
