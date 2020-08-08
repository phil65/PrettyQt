#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `prettyqt` package."""

import pytest
from prettyqt.utils import helpers


def test_string_to_num_array():
    assert helpers.string_to_num_array("1, 3, 5") == [1, 3, 5]
    with pytest.raises(ValueError):
        helpers.string_to_num_array("1, 2, f")


def test_cut_off_str():
    assert helpers.cut_off_str("abcdef", max_len=5) == "'a..."


def test_format_kwargs():
    dct = dict(a="a", b=1)
    assert helpers.format_kwargs(dct) == "a='a', b=1"
