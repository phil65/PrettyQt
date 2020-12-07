#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `prettyqt` package."""

import pickle
import pathlib
import inspect

import pytest

from prettyqt import custom_validators

clsmembers = inspect.getmembers(custom_validators, inspect.isclass)


@pytest.mark.parametrize("name, cls", clsmembers)
def test_pickle(name, cls):
    vale = cls()
    with open("data.pkl", "wb") as jar:
        pickle.dump(vale, jar)
    with open("data.pkl", "rb") as jar:
        vale = pickle.load(jar)


def test_pathvalidator():
    val = custom_validators.PathValidator()
    with open("data.pkl", "wb") as jar:
        pickle.dump(val, jar)
    with open("data.pkl", "rb") as jar:
        val = pickle.load(jar)
    assert val.is_valid_value(str(pathlib.Path.cwd()))
    assert not val.is_valid_value("abs")
    repr(val)
    assert val == custom_validators.PathValidator()
    assert val != custom_validators.NotZeroValidator()


def test_notzerovalidator():
    val = custom_validators.NotZeroValidator()
    assert val.is_valid_value("1")
    assert not val.is_valid_value("0")
    repr(val)
    assert val != custom_validators.PathValidator()
    assert val == custom_validators.NotZeroValidator()


def test_notemptyvalidator():
    val = custom_validators.NotEmptyValidator()
    assert val.is_valid_value("1")
    assert not val.is_valid_value("")
    repr(val)
    assert val != custom_validators.PathValidator()
    assert val == custom_validators.NotEmptyValidator()


def test_compositevalidator():
    val1 = custom_validators.NotEmptyValidator()
    val2 = custom_validators.NotZeroValidator()
    val = custom_validators.CompositeValidator([val1, val2])
    assert val != custom_validators.PathValidator()
    assert val == custom_validators.CompositeValidator([val1, val2])
    with open("data.pkl", "wb") as jar:
        pickle.dump(val, jar)
    with open("data.pkl", "rb") as jar:
        val = pickle.load(jar)
    assert val.is_valid_value("1")
    assert not val.is_valid_value("")
    assert not val.is_valid_value("0")
    val1 + val2
    repr(val)


def test_intlistvalidator():
    val = custom_validators.IntListValidator(allow_single=True)
    assert val.is_valid_value("1")
    assert val.is_valid_value("1,2")
    val = custom_validators.IntListValidator(allow_single=False)
    assert not val.is_valid_value("1")
    assert val.is_valid_value("1,2")
    repr(val)
    assert val != custom_validators.PathValidator()
    assert val == custom_validators.IntListValidator(allow_single=False)


def test_floatlistvalidator():
    val = custom_validators.FloatListValidator(allow_single=True)
    assert val.is_valid_value("1.0")
    assert val.is_valid_value("1.0,2")
    val = custom_validators.FloatListValidator(allow_single=False)
    assert not val.is_valid_value("1.0")
    assert val.is_valid_value("1.0,2")
    repr(val)
    assert val != custom_validators.PathValidator()
    assert val == custom_validators.FloatListValidator(allow_single=False)


def test_regexpatternvalidator():
    val = custom_validators.RegexPatternValidator()
    assert val.is_valid_value("[") is False
    assert val.is_valid_value("[0-9]") is True
    repr(val)
    assert val != custom_validators.PathValidator()
    assert val == custom_validators.RegexPatternValidator()
