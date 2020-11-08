#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `prettyqt` package."""

import pytest

from prettyqt import multimediawidgets
from prettyqt.utils import InvalidParamError


def test_videowidget(qapp):
    multimediawidgets.VideoWidget()


def test_graphicsvideoitem(qapp):
    item = multimediawidgets.GraphicsVideoItem()
    item.get_offset()
    item.get_native_size()
    item.get_size()
    item.set_aspect_ratio_mode("keep")
    with pytest.raises(InvalidParamError):
        item.set_aspect_ratio_mode("test")
    assert item.get_aspect_ratio_mode() == "keep"
