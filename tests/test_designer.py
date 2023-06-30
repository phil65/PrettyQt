"""Tests for `prettyqt` package."""

from prettyqt import core, designer


def test_abstractextensionfactory(qtbot):
    designer.AbstractExtensionFactory()


def test_pydesignertaskmenuextension(qtbot):
    parent = core.Object()
    designer.PyDesignerTaskMenuExtension(parent)
