"""designer module.

contains QtDesigner-based classes
"""
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

__all__ = [
    "PyDesignerCustomWidgetPlugin",
    "PyDesignerCustomWidgetCollectionPlugin",
    "PyDesignerCustomWidgetCollection",
    "AbstractExtensionFactory",
    "PyDesignerTaskMenuExtension",
]
