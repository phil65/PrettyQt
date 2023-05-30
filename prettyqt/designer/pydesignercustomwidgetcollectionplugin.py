from __future__ import annotations

from prettyqt import core
from prettyqt.qt import QtDesigner


class PyDesignerCustomWidgetCollectionPlugin(
    core.ObjectMixin, QtDesigner.QPyDesignerCustomWidgetCollectionPlugin
):
    def customWidgets(self):
        pass


if __name__ == "__main__":
    fact = PyDesignerCustomWidgetCollectionPlugin()
    new = dir(PyDesignerCustomWidgetCollectionPlugin())
    bie = dir(core.Object())
    c = [x for x in new if x not in bie]
