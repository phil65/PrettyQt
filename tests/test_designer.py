"""Tests for `prettyqt` package."""

from prettyqt import designer


def test_abstractextensionfactory(qtbot):
    designer.AbstractExtensionFactory()


# Segfault with PySide6
# def test_pydesignertaskmenuextension(qtbot):
#     parent = core.Object()
#     designer.PyDesignerTaskMenuExtension(parent)
