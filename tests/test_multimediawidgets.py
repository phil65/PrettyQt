#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `prettyqt` package."""

from prettyqt import multimediawidgets


def test_videowidget(qapp):
    multimediawidgets.VideoWidget()
