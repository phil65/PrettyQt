#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `prettyqt` package."""

import pytest


from prettyqt import widgets, core


@pytest.fixture
def response():
    """Sample pytest fixture.

    See more at: http://doc.pytest.org/en/latest/fixture.html
    """
    return widgets.Callout()


def test_settings():
    settings = core.Settings("1", "2")
    settings.set_value("test", "value")
    assert settings.contains("test")
    assert settings.value("test") == "value"


# def test_textbrowser():
#     app = widgets.Application.create_default_app()
#     reader = widgets.TextBrowser()
#     reader.show()
#     reader.close()
#     assert True
