#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `datacook` package."""

# import pytest

import pytest

from prettyqt import widgets


@pytest.fixture(scope="session")
def qapp():
    yield widgets.Application([])
