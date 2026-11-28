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
from .abstractformbuilder import AbstractFormBuilder, AbstractFormBuilderMixin
from .formbuilder import FormBuilder
from prettyqt.qt import QtDesigner

QT_MODULE = QtDesigner

__all__ = [
    "AbstractExtensionFactory",
    "AbstractFormBuilder",
    "AbstractFormBuilderMixin",
    "DesignerCustomWidgetInterface",
    "DesignerFormEditorInterface",
    "FormBuilder",
    "PyDesignerTaskMenuExtension",
]

if qt.API == "pyqt6":
    __all__ += [
        "PyDesignerCustomWidgetCollectionPlugin",
        "PyDesignerCustomWidgetPlugin",
    ]
else:
    __all__ += ["PyDesignerCustomWidgetCollection"]
