"""Tests for `prettyqt` package."""

import pytest

from prettyqt import designer, qt


def test_abstractextensionfactory(qtbot):
    designer.AbstractExtensionFactory()


def test_designer_exports():
    assert "AbstractFormBuilderMixin" in designer.__all__
    for name in designer.__all__:
        assert hasattr(designer, name)
    if qt.API == "pyqt6":
        assert "PyDesignerCustomWidgetPlugin" in designer.__all__
        assert "PyDesignerCustomWidgetCollectionPlugin" in designer.__all__
        assert "PyDesignerCustomWidgetCollection" not in designer.__all__
    else:
        assert "PyDesignerCustomWidgetCollection" in designer.__all__
        assert "PyDesignerCustomWidgetPlugin" not in designer.__all__
        assert "PyDesignerCustomWidgetCollectionPlugin" not in designer.__all__


def test_designer_plugins(qapp):
    if qt.API == "pyqt6":
        plugin = designer.PyDesignerCustomWidgetPlugin()
        assert plugin is not None
        collection = designer.PyDesignerCustomWidgetCollectionPlugin()
        with pytest.raises(NotImplementedError):
            collection.customWidgets()
    else:
        assert hasattr(designer, "PyDesignerCustomWidgetCollection")


def test_pydesignertaskmenuextension_methods():
    with pytest.raises(NotImplementedError):
        designer.PyDesignerTaskMenuExtension.preferredEditAction(None)  # ty: ignore[invalid-argument-type]
    with pytest.raises(NotImplementedError):
        designer.PyDesignerTaskMenuExtension.taskActions(None)  # ty: ignore[invalid-argument-type]
