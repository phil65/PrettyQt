from __future__ import annotations

from prettyqt import widgets
from prettyqt.qt import QtWidgets


QtWidgets.QGraphicsProxyWidget.__bases__ = (widgets.GraphicsWidget,)


class GraphicsProxyWidget(QtWidgets.QGraphicsProxyWidget):

    pass
