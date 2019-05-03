#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `prettyqt` package."""

from prettyqt import widgets, gui, core
from qtpy import QtCore, QtGui

test_widget = widgets.Widget()


def test_buttondelegate():
    widget = widgets.ButtonDelegate(parent=None)
    widget.setEditorData(widgets.Widget(), None)
    widget.createEditor(None, None, QtCore.QModelIndex())
    widget.currentIndexChanged()


def test_colorchooserbutton():
    btn = widgets.ColorChooserButton()
    btn.set_color("green")
    btn.show()
    btn.color_updated.connect(print)


def test_filechooserbutton():
    btn = widgets.FileChooserButton()
    btn.show()
    btn.file_updated.connect(print)


def test_codeeditor():
    editor = widgets.CodeEditor()
    assert editor.text() == ""
    editor.line_area_width()
    editor.set_syntax("python")
    event = QtGui.QResizeEvent(core.Size(10, 10), core.Size(20, 20))
    editor.resizeEvent(event)
    event = QtGui.QPaintEvent(core.Rect(0, 0, 20, 20))
    editor.line_area_paintevent(event)


def test_imageviewer():
    widget = widgets.ImageViewer()
    widget.show()


def test_markdownwidget():
    widget = widgets.MarkdownWindow()
    widget.show()


def test_popupinfo():
    popup = widgets.PopupInfo()
    popup.show_popup("test")


def test_selectionwidget():
    widget = widgets.SelectionWidget()
    items = {"Semicolon": ";",
             "Tab": "\t",
             "Comma": ","}
    widget.add_items(items)
    widget.add_custom(regex=r"\S{1}")
    choice = widget.current_choice()
    assert(choice == ";")


def test_spanslider(qtbot):
    slider = widgets.SpanSlider()
    qtbot.addWidget(slider)
    slider.set_lower_value(10)
    slider.set_upper_value(20)
    slider.set_lower_pos(15)
    slider.set_upper_pos(25)
    assert(slider.lower_value == 15)
    assert(slider.upper_value == 25)
    slider.set_lower_value(12)
    slider.set_upper_pos(20)
    color = gui.Color("blue")
    slider.set_left_color(color)
    slider.set_right_color(color)
    slider.swap_controls()
    slider.trigger_action(slider.SliderNoAction, True)
    slider.trigger_action(slider.SliderSingleStepAdd, True)
    slider.paintEvent(None)
    slider.pixel_pos_to_value(100)
    slider.draw_span(gui.Painter(), core.Rect())
    slider.move_pressed_handle()
    slider.show()
    qtbot.mouseClick(slider, QtCore.Qt.LeftButton)
    qtbot.mouseMove(slider, core.Point(20, 20))
    assert(slider.movement_mode is None)


def test_waitingspinner():
    spinner = widgets.WaitingSpinner(parent=test_widget)
    spinner.paintEvent(None)
    spinner.set_line_num(2)
    assert spinner.line_num() == 2
    spinner.set_line_length(2)
    assert spinner.line_length() == 2
    spinner.set_line_width(2)
    assert spinner.line_width() == 2
    spinner.set_inner_radius(2)
    assert spinner.inner_radius() == 2
    spinner.set_color("black")
    spinner.set_revolutions_per_second(2)
    spinner.set_trail_fade_percentage(2)
    spinner.set_minimum_trail_opacity(2)
    spinner.rotate()
    spinner.start()
    spinner.stop()
    spinner.update_position()
