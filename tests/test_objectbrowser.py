#!/usr/bin/env python

"""Tests for `prettyqt` package."""


from prettyqt.objbrowser import objectbrowser


def test_objectbrowser(qtbot):
    struct = dict(a={1, 2, frozenset([1, 2])})
    browser = objectbrowser.ObjectBrowser(struct)
    browser.show()
    browser.close()
