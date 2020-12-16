from qtpy import QtWidgets

from prettyqt import widgets
from prettyqt.utils import bidict


CHECK_TYPE = bidict(
    not_checkable=QtWidgets.QStyleOptionMenuItem.NotCheckable,
    exclusive=QtWidgets.QStyleOptionMenuItem.Exclusive,
    non_exclusive=QtWidgets.QStyleOptionMenuItem.NonExclusive,
)

MENU_ITEM_TYPE = bidict(
    normal=QtWidgets.QStyleOptionMenuItem.Normal,
    default_item=QtWidgets.QStyleOptionMenuItem.DefaultItem,
    separator=QtWidgets.QStyleOptionMenuItem.Separator,
    sub_menu=QtWidgets.QStyleOptionMenuItem.SubMenu,
    scroller=QtWidgets.QStyleOptionMenuItem.Scroller,
    tear_off=QtWidgets.QStyleOptionMenuItem.TearOff,
    margin=QtWidgets.QStyleOptionMenuItem.Margin,
    empty_area=QtWidgets.QStyleOptionMenuItem.EmptyArea,
)


QtWidgets.QStyleOptionMenuItem.__bases__ = (widgets.StyleOption,)


class StyleOptionMenuItem(QtWidgets.QStyleOptionMenuItem):
    pass
