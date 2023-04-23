from __future__ import annotations

from prettyqt import widgets
from prettyqt.qt import QtWidgets


class GraphicsProxyWidget(widgets.GraphicsWidgetMixin, QtWidgets.QGraphicsProxyWidget):
    pass


if __name__ == "__main__":
    app = widgets.app()
    w = GraphicsProxyWidget()
