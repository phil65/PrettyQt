"""Tests for `prettyqt` package."""

from prettyqt import gui, test, widgets


def test_buttondelegate(qtbot):
    model = gui.StandardItemModel()
    test.AbstractItemModelTester(model)


def test_signalspy(qtbot):
    widget = widgets.Widget()
    test.SignalSpy(widget.windowIconChanged)
