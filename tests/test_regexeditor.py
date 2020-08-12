#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `prettyqt` package."""


from prettyqt.custom_widgets import regexeditor


def test_regexeditor(qtbot):
    teststring = "aa356aa356aa356aa356aa356aa356aa356aa3a356aa356"
    widget = regexeditor.RegexEditorWidget(regex="aa[0-9]", teststring=teststring)
    widget.show()
    widget.close()
