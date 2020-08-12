#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `prettyqt` package."""

# import regex as re

from prettyqt import custom_models, widgets


def test_transposeproxymodel():
    source = widgets.FileSystemModel()
    model = custom_models.TransposeProxyModel(source)
    idx = model.index(0, 0)
    model.data(idx)
    model.columnCount()
    model.rowCount()


def test_regexmatchesmodel(qtmodeltester):
    # comp = re.compile("[0-9]")
    # text = "aa356aa356"
    matches = []  # list(comp.finditer(text))
    model = custom_models.RegexMatchesModel(matches)
    qtmodeltester.check(model, force_py=True)
