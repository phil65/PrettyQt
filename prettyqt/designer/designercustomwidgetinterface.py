from __future__ import annotations

from prettyqt.qt import QtDesigner


class DesignerCustomWidgetInterface(QtDesigner.QDesignerCustomWidgetInterface):
    pass


if __name__ == "__main__":
    interface = DesignerCustomWidgetInterface()
