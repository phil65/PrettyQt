from qtpy import QtWidgets

from prettyqt import widgets


QtWidgets.QStyleOptionTabWidgetFrame.__bases__ = (widgets.StyleOption,)


class StyleOptionTabWidgetFrame(QtWidgets.QStyleOptionTabWidgetFrame):
    pass
