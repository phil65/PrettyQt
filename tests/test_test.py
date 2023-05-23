"""Tests for `prettyqt` package."""

from prettyqt import gui, test, widgets


def test_buttondelegate(qtbot):
    model = gui.StandardItemModel()
    tester = test.AbstractItemModelTester(model)


def test_signalspy(qtbot):
    widget = widgets.Widget()
    spy = test.SignalSpy(widget.windowIconChanged)
