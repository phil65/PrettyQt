"""Tests for `prettyqt` package."""

import pytest


ipython = pytest.importorskip("prettyqt.ipython")


def test_inprocessipythonwidget(qapp):
    widget = ipython.InProcessIPythonWidget()
    widget.push_vars(dict(a=1))
    assert widget.eval("a") == 1


def test_outofprocessipythonwidget(qapp):
    widget = ipython.OutOfProcessIPythonWidget()
    assert widget is not None
