"""Tests for `prettyqt` package."""

import pytest

from prettyqt.utils import InvalidParamError


scintilla = pytest.importorskip("prettyqt.scintilla")


def test_sciscintilla_basic(qtbot):
    assert hasattr(scintilla, "QsciScintilla")
    widget = scintilla.SciScintilla()
    widget.set_value("line 1\nline 2\nline 3")
    assert widget.get_value() == "line 1\nline 2\nline 3"
    widget.scroll_to_bottom()
    widget.highlight_current_line(True, None)
    widget.highlight_current_line(True, "red")
    widget.set_brace_matching("strict")
    widget.set_brace_matching(None)
    widget.set_wrap_mode("word")
    widget.set_wrap_mode(None)


def test_sciscintilla_empty_scroll_to_bottom(qtbot):
    widget = scintilla.SciScintilla()
    widget.scroll_to_bottom()


def test_sciscintilla_syntaxhighlighter(qtbot):
    widget = scintilla.SciScintilla()
    for lang in (
        "python",
        "avs",
        "intel_hex",
        "masm",
        "nasm",
        "srec",
        "tek_hex",
    ):
        widget.set_syntaxhighlighter(lang)
        assert widget.language == lang
    with pytest.raises(InvalidParamError):
        widget.set_syntaxhighlighter("nonexistent_lang")


def test_sciscintilla_toggle_marker(qtbot):
    widget = scintilla.SciScintilla()
    widget.set_value("line 0\nline 1")
    widget.define_marker("circle", 1)
    widget.define_marker("rectangle", 2)
    widget.toggle_marker(0, 1)
    assert widget.markersAtLine(0) & (1 << 1)
    assert not (widget.markersAtLine(0) & (1 << 2))
    # Toggling marker 2 on the same line should ADD marker 2, not delete it!
    widget.toggle_marker(0, 2)
    assert widget.markersAtLine(0) & (1 << 1)
    assert widget.markersAtLine(0) & (1 << 2)
    # Toggling marker 1 again removes only marker 1
    widget.toggle_marker(0, 1)
    assert not (widget.markersAtLine(0) & (1 << 1))
    assert widget.markersAtLine(0) & (1 << 2)
