#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `prettyqt` package."""

import pytest

from prettyqt import widgets

app = widgets.Application.create_default_app()


def test_buttondelegate():
    action = widgets.ButtonDelegate(parent=None)


def test_callout():
    action = widgets.Callout()


def test_imageviewer():
    action = widgets.ImageViewer()


def test_markdownwidget():
    action = widgets.MarkdownWindow()


def test_popupinfo():
    action = widgets.PopupInfo()


def test_selectionwidget():
    action = widgets.SelectionWidget()


def test_spanslider():
    action = widgets.SpanSlider()


def test_waitingspinner():
    action = widgets.WaitingSpinner(parent=None)
