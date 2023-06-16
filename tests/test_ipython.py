"""Tests for `prettyqt` package."""

import pytest


ipython = pytest.importorskip("prettyqt.ipython")


# TODO: this somehow interferes with AbstractItemModel.__getitem__ for whatever reason...
# Need to investigate.

# def test_inprocessipythonwidget(qtbot):
#     widget = ipython.InProcessIPythonWidget()
#     qtbot.addWidget(widget)
#     widget.push_vars(dict(a=1))
#     assert widget.eval("a") == 1


# def test_outofprocessipythonwidget(qapp):
#     widget = ipython.OutOfProcessIPythonWidget()
#     assert widget is not None
