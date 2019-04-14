#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `prettyqt` package."""

import pytest

from prettyqt import gui


def test_color():
    color = gui.Color()
    color.set_color("gray")


def test_icon():
    color = gui.Icon()
    color.set_size(20)
