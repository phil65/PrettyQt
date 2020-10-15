#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `prettyqt` package."""

import pytest

from prettyqt import webenginecore
from prettyqt.utils import InvalidParamError


def test_webengineurlscheme():
    scheme = webenginecore.WebEngineUrlScheme()
    scheme.set_name("test")
    assert scheme.get_name() == "test"
    scheme.set_syntax("host")
    with pytest.raises(InvalidParamError):
        scheme.set_syntax("test")
    assert scheme.get_syntax() == "host"
