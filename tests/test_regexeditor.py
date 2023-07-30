"""Tests for `prettyqt` package."""

import pytest

from prettyqt import qt
from prettyqt.custom_widgets import regexeditor


@pytest.mark.skipif(qt.API == "pyside6", reason="Leads to Segfault later on in tests")
def test_regexeditor(qtbot):
    teststring = "aa356aa356aa356aa356aa356aa356aa356aa3a356aa356"
    widget = regexeditor.RegexEditorWidget(regex="aa[0-9]", teststring=teststring)
    widget.show()
    widget.close()
