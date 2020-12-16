"""Tests for `prettyqt` package."""

import pytest
import qtpy

from prettyqt.utils import InvalidParamError


@pytest.mark.skipif(qtpy.API == "pyside2", reason="Only supported in PyQt5")
def test_sciscintilla(qtbot):
    from prettyqt import gui, scintilla

    widget = scintilla.SciScintilla()
    widget.define_marker("circle", 0)
    with pytest.raises(InvalidParamError):
        widget.define_marker("test", 0)
    widget.set_marker_background_color("red", 0)
    widget.set_margins_background_color("green")
    widget.highlight_current_line("blue")
    widget.set_brace_matching("sloppy")
    with pytest.raises(InvalidParamError):
        widget.set_brace_matching("test")
    widget.set_text("test")
    assert widget.get_value() == "test"
    widget.set_syntaxhighlighter("python")
    widget.scroll_to_bottom()
    widget.append_text("test", newline=False)
    assert widget.text() == "testtest"
    widget.append_text("test", newline=True)
    assert widget.text() == "testtest\ntest"
    widget.set_font(gui.Font("Consolas"))
    widget.set_read_only()
    widget.set_value("test")
