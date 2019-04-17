#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `prettyqt` package."""

import pytest

from prettyqt import widgets, gui

app = widgets.Application.create_default_app()


def test_buttondelegate():
    delegate = widgets.ButtonDelegate(parent=None)


def test_callout():
    callout = widgets.Callout()


def test_imageviewer():
    widget = widgets.ImageViewer()


def test_markdownwidget():
    widget = widgets.MarkdownWindow()


def test_popupinfo():
    popup = widgets.PopupInfo()


def test_selectionwidget():
    widget = widgets.SelectionWidget()
    items = {"Semicolon": ";",
             "Tab": "\t",
             "Comma": ","}
    widget.add_items(items)
    widget.add_custom(regex=r"\S{1}")
    choice = widget.current_choice()
    assert(choice == ";")


def test_spanslider():
    slider = widgets.SpanSlider()
    slider.set_lower_value(10)
    slider.set_upper_value(20)
    slider.set_lower_pos(15)
    slider.set_upper_pos(17)
    assert(slider.lower_value == 15)
    color = gui.Color("blue").lighter(150)
    slider.set_left_color(color)
    slider.set_right_color(color)

def test_waitingspinner():
    action = widgets.WaitingSpinner(parent=None)
