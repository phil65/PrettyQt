from qtpy import QtSvg

from prettyqt import widgets


QtSvg.QGraphicsSvgItem.__bases__ = (widgets.GraphicsObject,)


class GraphicsSvgItem(QtSvg.QGraphicsSvgItem):
    pass
