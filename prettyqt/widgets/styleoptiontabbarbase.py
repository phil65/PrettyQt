from qtpy import QtWidgets

from prettyqt import widgets


QtWidgets.QStyleOptionTabBarBase.__bases__ = (widgets.StyleOption,)


class StyleOptionTabBarBase(QtWidgets.QStyleOptionTabBarBase):
    pass
