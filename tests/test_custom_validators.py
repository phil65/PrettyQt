#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `prettyqt` package."""

import pickle
import pathlib

from prettyqt import custom_validators, widgets

test_widget = widgets.Widget()


def test_pathvalidator():
    val = custom_validators.PathValidator()
    with open("data.pkl", "wb") as jar:
        pickle.dump(val, jar)
    with open("data.pkl", "rb") as jar:
        val = pickle.load(jar)
    assert val.is_valid_value(str(pathlib.Path.cwd()))
    assert not val.is_valid_value("abs")


def test_notzerovalidator():
    val = custom_validators.NotZeroValidator()
    with open("data.pkl", "wb") as jar:
        pickle.dump(val, jar)
    with open("data.pkl", "rb") as jar:
        val = pickle.load(jar)
    assert val.is_valid_value("1")
    assert not val.is_valid_value("0")


def test_notemptyvalidator():
    val = custom_validators.NotEmptyValidator()
    with open("data.pkl", "wb") as jar:
        pickle.dump(val, jar)
    with open("data.pkl", "rb") as jar:
        val = pickle.load(jar)
    assert val.is_valid_value("1")
    assert not val.is_valid_value("")


def test_compositevalidator():
    val1 = custom_validators.NotEmptyValidator()
    val2 = custom_validators.NotZeroValidator()
    val = custom_validators.CompositeValidator([val1, val2])
    with open("data.pkl", "wb") as jar:
        pickle.dump(val, jar)
    with open("data.pkl", "rb") as jar:
        val = pickle.load(jar)
    assert val.is_valid_value("1")
    assert not val.is_valid_value("")
    assert not val.is_valid_value("0")
    val1 + val2
