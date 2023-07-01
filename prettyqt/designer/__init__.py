from __future__ import annotations

from prettyqt.qt.QtDesigner import *  # noqa: F403

from prettyqt import qt

if qt.API == "pyqt6":
    from .pydesignercustomwidgetcollectionplugin import (
        PyDesignerCustomWidgetCollectionPlugin,
    )
    from .pydesignercustomwidgetplugin import PyDesignerCustomWidgetPlugin
else:
    from .pydesignercustomwidgetcollection import PyDesignerCustomWidgetCollection

from .abstractextensionfactory import AbstractExtensionFactory
from .pydesignertaskmenuextension import PyDesignerTaskMenuExtension
from .designercustomwidgetinterface import DesignerCustomWidgetInterface
from .designerformeditorinterface import DesignerFormEditorInterface
from .abstractformbuilder import AbstractFormBuilder
from .formbuilder import FormBuilder

__all__ = [
    "PyDesignerCustomWidgetPlugin",
    "PyDesignerCustomWidgetCollectionPlugin",
    "PyDesignerCustomWidgetCollection",
    "AbstractExtensionFactory",
    "PyDesignerTaskMenuExtension",
    "DesignerCustomWidgetInterface",
    "DesignerFormEditorInterface",
    "AbstractFormBuilder",
    "FormBuilder",
]
