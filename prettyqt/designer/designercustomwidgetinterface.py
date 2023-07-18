from __future__ import annotations

from prettyqt.qt import QtDesigner


class DesignerCustomWidgetInterface(QtDesigner.QDesignerCustomWidgetInterface):
    """Enables Qt Designer to access and construct custom widgets."""


if __name__ == "__main__":
    interface = DesignerCustomWidgetInterface()
