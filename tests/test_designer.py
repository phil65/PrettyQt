"""Tests for `prettyqt` package."""

from prettyqt import core, designer


def test_abstractextensionfactory(qtbot):
    factory = designer.AbstractExtensionFactory()


def test_pydesignertaskmenuextension(qtbot):
    parent = core.Object()
    extension = designer.PyDesignerTaskMenuExtension(parent)
