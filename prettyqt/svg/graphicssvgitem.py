from __future__ import annotations

from prettyqt import widgets
from prettyqt.qt import QtSvg


QtSvg.QGraphicsSvgItem.__bases__ = (widgets.GraphicsObject,)


class GraphicsSvgItem(QtSvg.QGraphicsSvgItem):
    pass
