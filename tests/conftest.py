#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `datacook` package."""

# import pytest

import pytest

from prettyqt import widgets


@pytest.fixture(scope="session")
def qapp():
    app = widgets.Application([])
    app.set_metadata(app_name="test",
                     app_version="1.0.0",
                     org_name="test",
                     org_domain="test")
    yield app
