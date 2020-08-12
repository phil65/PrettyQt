#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `prettyqt` package."""


from prettyqt.objbrowser import objectbrowser


def test_objectbrowser(qtbot):
    struct = dict(a=set([1, 2, frozenset([1, 2])]))
    browser = objectbrowser.ObjectBrowser(struct)
    browser.show()
    browser.close()
