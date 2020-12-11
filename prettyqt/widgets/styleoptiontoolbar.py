from qtpy import QtWidgets

from prettyqt import widgets
from prettyqt.utils import bidict


TOOLBAR_FEATURE = bidict(
    none=QtWidgets.QStyleOptionToolBar.ToolBarFeature(0),
    movable=QtWidgets.QStyleOptionToolBar.Movable,
)

QtWidgets.QStyleOptionToolBar.__bases__ = (widgets.StyleOption,)


class StyleOptionToolBar(QtWidgets.QStyleOptionToolBar):
    pass
