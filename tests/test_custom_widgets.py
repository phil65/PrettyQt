#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `prettyqt` package."""

import pickle

from qtpy import QtCore, QtGui

from prettyqt import core, custom_widgets, gui, widgets

test_widget = widgets.Widget()


def test_buttondelegate():
    widget = custom_widgets.ButtonDelegate(parent=None)
    widget.setEditorData(widgets.Widget(), None)
    widget.createEditor(None, None, QtCore.QModelIndex())
    widget.currentIndexChanged()


def test_colorchooserbutton():
    btn = custom_widgets.ColorChooserButton()
    btn.set_color("green")
    with open("data.pkl", "wb") as jar:
        pickle.dump(btn, jar)
    with open("data.pkl", "rb") as jar:
        btn = pickle.load(jar)
    btn.show()


def test_filechooserbutton():
    btn = custom_widgets.FileChooserButton()
    with open("data.pkl", "wb") as jar:
        pickle.dump(btn, jar)
    with open("data.pkl", "rb") as jar:
        btn = pickle.load(jar)
    btn.show()


def test_codeeditor():
    editor = custom_widgets.CodeEditor()
    assert editor.text() == ""
    editor.line_area_width()
    editor.set_syntax("python")
    event = QtGui.QResizeEvent(core.Size(10, 10), core.Size(20, 20))
    editor.resizeEvent(event)
    event = QtGui.QPaintEvent(core.Rect(0, 0, 20, 20))
    editor.line_area_paintevent(event)


def test_imageviewer():
    widget = custom_widgets.ImageViewer()
    widget.show()


def test_flowlayout():
    widget = widgets.Widget()
    layout = custom_widgets.FlowLayout()
    layout += widgets.PushButton("Short")
    layout += widgets.PushButton("Longer")
    layout += widgets.PushButton("Different text")
    layout += widgets.PushButton("More text")
    layout += widgets.PushButton("Even longer button text")
    widget.setLayout(layout)
    widget.show()


def test_markdownwidget():
    widget = custom_widgets.MarkdownWindow()
    widget.show()


def test_popupinfo():
    popup = custom_widgets.PopupInfo()
    popup.show_popup("test")


def test_selectionwidget():
    widget = custom_widgets.SelectionWidget()
    items = {"Semicolon": ";",
             "Tab": "\t",
             "Comma": ","}
    widget.add_items(items)
    widget.add_custom(label="test", regex=r"\S{1}")
    choice = widget.current_choice()
    assert(choice == ";")


def test_spanslider(qtbot):
    slider = custom_widgets.SpanSlider()
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
    assert(slider.movement_mode == "free")


def test_waitingspinner():
    spinner = custom_widgets.WaitingSpinner(parent=test_widget)
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
