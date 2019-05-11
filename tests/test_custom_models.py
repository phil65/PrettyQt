#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `prettyqt` package."""

from prettyqt import custom_models, widgets


def test_transposeproxymodel():
    source = widgets.FileSystemModel()
    model = custom_models.TransposeProxyModel(source)
    idx = model.index(0, 0)
    model.data(idx)
    model.columnCount()
    model.rowCount()
