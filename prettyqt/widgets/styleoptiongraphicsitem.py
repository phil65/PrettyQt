from qtpy import QtWidgets

from prettyqt import widgets


QtWidgets.QStyleOptionGraphicsItem.__bases__ = (widgets.StyleOption,)


class StyleOptionGraphicsItem(QtWidgets.QStyleOptionGraphicsItem):
    pass
