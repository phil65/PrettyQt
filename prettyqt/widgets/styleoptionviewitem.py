from qtpy import QtWidgets

from prettyqt import widgets
from prettyqt.utils import bidict


POSITION = bidict(
    left=QtWidgets.QStyleOptionViewItem.Left,
    right=QtWidgets.QStyleOptionViewItem.Right,
    top=QtWidgets.QStyleOptionViewItem.Top,
    bottom=QtWidgets.QStyleOptionViewItem.Bottom,
)

VIEW_ITEM_FEATURE = bidict(
    none=QtWidgets.QStyleOptionViewItem.ViewItemFeature(0),
    wrap_text=QtWidgets.QStyleOptionViewItem.WrapText,
    alternate=QtWidgets.QStyleOptionViewItem.Alternate,
    has_check_indicator=QtWidgets.QStyleOptionViewItem.HasCheckIndicator,
    has_display=QtWidgets.QStyleOptionViewItem.HasDisplay,
    has_decoration=QtWidgets.QStyleOptionViewItem.HasDecoration,
)

VIEW_ITEM_POSITION = bidict(
    invalid=QtWidgets.QStyleOptionViewItem.Invalid,
    beginning=QtWidgets.QStyleOptionViewItem.Beginning,
    middle=QtWidgets.QStyleOptionViewItem.Middle,
    end=QtWidgets.QStyleOptionViewItem.End,
    only_one=QtWidgets.QStyleOptionViewItem.OnlyOne,
)

QtWidgets.QStyleOptionViewItem.__bases__ = (widgets.StyleOption,)


class StyleOptionViewItem(QtWidgets.QStyleOptionViewItem):
    pass
