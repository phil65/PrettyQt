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
from prettyqt.qt import QtDesigner

QT_MODULE = QtDesigner

__all__ = [
    "AbstractExtensionFactory",
    "AbstractFormBuilder",
    "DesignerCustomWidgetInterface",
    "DesignerFormEditorInterface",
    "FormBuilder",
    "PyDesignerCustomWidgetCollection",
    "PyDesignerCustomWidgetCollectionPlugin",
    "PyDesignerCustomWidgetPlugin",
    "PyDesignerTaskMenuExtension",
]
