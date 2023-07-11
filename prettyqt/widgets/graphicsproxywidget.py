from __future__ import annotations

from prettyqt import widgets


class GraphicsProxyWidget(widgets.GraphicsWidgetMixin, widgets.QGraphicsProxyWidget):
    """Proxy layer for embedding a QWidget in a QGraphicsScene."""


if __name__ == "__main__":
    app = widgets.app()
    w = GraphicsProxyWidget()
