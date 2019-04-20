#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `prettyqt` package."""

from prettyqt import widgets, gui, core
from qtpy import QtCore

app = widgets.Application.create_default_app()
test_widget = widgets.Widget()


def test_buttondelegate():
    widgets.ButtonDelegate(parent=None)


def test_callout():
    callout = widgets.Callout()
    # callout.boundingRect()
    callout.set_text("test")


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
    color = gui.Color("blue").lighter(150)
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
    spinner.start()
    spinner.stop()
    spinner.update_position()
