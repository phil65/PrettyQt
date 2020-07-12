#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `prettyqt` package."""

from prettyqt import scintilla, gui


def test_sciscintilla(qtbot):
    widget = scintilla.SciScintilla()
    widget.define_marker("circle", 0)
    widget.set_marker_background_color("red", 0)
    widget.set_margins_background_color("green")
    widget.highlight_current_line("blue")
    widget.set_brace_matching("sloppy")
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
