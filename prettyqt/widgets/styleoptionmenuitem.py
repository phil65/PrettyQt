from __future__ import annotations

from prettyqt import widgets
from prettyqt.qt import QtWidgets
from prettyqt.utils import bidict


CHECK_TYPE = bidict(
    not_checkable=QtWidgets.QStyleOptionMenuItem.CheckType.NotCheckable,
    exclusive=QtWidgets.QStyleOptionMenuItem.CheckType.Exclusive,
    non_exclusive=QtWidgets.QStyleOptionMenuItem.CheckType.NonExclusive,
)

MENU_ITEM_TYPE = bidict(
    normal=QtWidgets.QStyleOptionMenuItem.MenuItemType.Normal,
    default_item=QtWidgets.QStyleOptionMenuItem.MenuItemType.DefaultItem,
    separator=QtWidgets.QStyleOptionMenuItem.MenuItemType.Separator,
    sub_menu=QtWidgets.QStyleOptionMenuItem.MenuItemType.SubMenu,
    scroller=QtWidgets.QStyleOptionMenuItem.MenuItemType.Scroller,
    tear_off=QtWidgets.QStyleOptionMenuItem.MenuItemType.TearOff,
    margin=QtWidgets.QStyleOptionMenuItem.MenuItemType.Margin,
    empty_area=QtWidgets.QStyleOptionMenuItem.MenuItemType.EmptyArea,
)


QtWidgets.QStyleOptionMenuItem.__bases__ = (widgets.StyleOption,)


class StyleOptionMenuItem(QtWidgets.QStyleOptionMenuItem):
    pass
