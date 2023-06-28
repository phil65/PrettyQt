from __future__ import annotations

from prettyqt import widgets


class GraphicsProxyWidget(widgets.GraphicsWidgetMixin, widgets.QGraphicsProxyWidget):
    pass


if __name__ == "__main__":
    app = widgets.app()
    w = GraphicsProxyWidget()
