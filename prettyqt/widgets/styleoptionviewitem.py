from __future__ import annotations

from prettyqt import widgets
from prettyqt.qt import QtWidgets
from prettyqt.utils import bidict


POSITION = bidict(
    left=QtWidgets.QStyleOptionViewItem.Position.Left,
    right=QtWidgets.QStyleOptionViewItem.Position.Right,
    top=QtWidgets.QStyleOptionViewItem.Position.Top,
    bottom=QtWidgets.QStyleOptionViewItem.Position.Bottom,
)

VIEW_ITEM_FEATURE = bidict(
    none=QtWidgets.QStyleOptionViewItem.ViewItemFeature(0),  # type: ignore
    wrap_text=QtWidgets.QStyleOptionViewItem.ViewItemFeature.WrapText,
    alternate=QtWidgets.QStyleOptionViewItem.ViewItemFeature.Alternate,
    has_check_indicator=QtWidgets.QStyleOptionViewItem.ViewItemFeature.HasCheckIndicator,
    has_display=QtWidgets.QStyleOptionViewItem.ViewItemFeature.HasDisplay,
    has_decoration=QtWidgets.QStyleOptionViewItem.ViewItemFeature.HasDecoration,
)

VIEW_ITEM_POSITION = bidict(
    invalid=QtWidgets.QStyleOptionViewItem.ViewItemPosition.Invalid,
    beginning=QtWidgets.QStyleOptionViewItem.ViewItemPosition.Beginning,
    middle=QtWidgets.QStyleOptionViewItem.ViewItemPosition.Middle,
    end=QtWidgets.QStyleOptionViewItem.ViewItemPosition.End,
    only_one=QtWidgets.QStyleOptionViewItem.ViewItemPosition.OnlyOne,
)

QtWidgets.QStyleOptionViewItem.__bases__ = (widgets.StyleOption,)


class StyleOptionViewItem(QtWidgets.QStyleOptionViewItem):
    pass
