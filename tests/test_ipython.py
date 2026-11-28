"""Tests for `prettyqt.ipython`."""

import pytest


ipython = pytest.importorskip("prettyqt.ipython")


def test_inprocessipythonwidget(qtbot):
    widget = ipython.InProcessIPythonWidget()
    qtbot.addWidget(widget)
    try:
        widget.push_vars({"a": 1})
        assert widget.eval("a") == 1
        assert widget.eval("nonexistent_var_xyz") is None
        assert widget.get_completion_mode() == "droplist"
        widget.print_text("hello")
        widget.clear()
    finally:
        widget.shutdown()


# Note: OutOfProcessIPythonWidget spawns a multiprocessing child running
# IPython.embed_kernel(..., gui="qt6") and polls up to 50s for a connection file,
# which is unsuitable for headless unit tests.
