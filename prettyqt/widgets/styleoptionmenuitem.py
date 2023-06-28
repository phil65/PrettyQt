from __future__ import annotations

from prettyqt import widgets
from prettyqt.utils import bidict


CHECK_TYPE = bidict(
    not_checkable=widgets.QStyleOptionMenuItem.CheckType.NotCheckable,
    exclusive=widgets.QStyleOptionMenuItem.CheckType.Exclusive,
    non_exclusive=widgets.QStyleOptionMenuItem.CheckType.NonExclusive,
)

MENU_ITEM_TYPE = bidict(
    normal=widgets.QStyleOptionMenuItem.MenuItemType.Normal,
    default_item=widgets.QStyleOptionMenuItem.MenuItemType.DefaultItem,
    separator=widgets.QStyleOptionMenuItem.MenuItemType.Separator,
    sub_menu=widgets.QStyleOptionMenuItem.MenuItemType.SubMenu,
    scroller=widgets.QStyleOptionMenuItem.MenuItemType.Scroller,
    tear_off=widgets.QStyleOptionMenuItem.MenuItemType.TearOff,
    margin=widgets.QStyleOptionMenuItem.MenuItemType.Margin,
    empty_area=widgets.QStyleOptionMenuItem.MenuItemType.EmptyArea,
)


class StyleOptionMenuItem(widgets.StyleOptionMixin, widgets.QStyleOptionMenuItem):
    pass
