from __future__ import annotations

from typing import Literal

from prettyqt import constants, widgets
from prettyqt.qt import QtWidgets
from prettyqt.utils import bidict


POSITION = bidict(
    left=QtWidgets.QStyleOptionViewItem.Position.Left,
    right=QtWidgets.QStyleOptionViewItem.Position.Right,
    top=QtWidgets.QStyleOptionViewItem.Position.Top,
    bottom=QtWidgets.QStyleOptionViewItem.Position.Bottom,
)

PositionStr = Literal["left", "right", "top", "bottom"]

VIEW_ITEM_FEATURE = bidict(
    none=QtWidgets.QStyleOptionViewItem.ViewItemFeature(0),  # type: ignore
    wrap_text=QtWidgets.QStyleOptionViewItem.ViewItemFeature.WrapText,
    alternate=QtWidgets.QStyleOptionViewItem.ViewItemFeature.Alternate,
    has_check_indicator=QtWidgets.QStyleOptionViewItem.ViewItemFeature.HasCheckIndicator,
    has_display=QtWidgets.QStyleOptionViewItem.ViewItemFeature.HasDisplay,
    has_decoration=QtWidgets.QStyleOptionViewItem.ViewItemFeature.HasDecoration,
)

ViewItemFeatureStr = Literal[
    "none",
    "wrap_text",
    "alternate",
    "has_check_indicator",
    "has_display",
    "has_decoration",
]

VIEW_ITEM_POSITION = bidict(
    invalid=QtWidgets.QStyleOptionViewItem.ViewItemPosition.Invalid,
    beginning=QtWidgets.QStyleOptionViewItem.ViewItemPosition.Beginning,
    middle=QtWidgets.QStyleOptionViewItem.ViewItemPosition.Middle,
    end=QtWidgets.QStyleOptionViewItem.ViewItemPosition.End,
    only_one=QtWidgets.QStyleOptionViewItem.ViewItemPosition.OnlyOne,
)

ViewItemPositionStr = Literal["invalid", "beginning", "middle", "end", "only_one"]


class StyleOptionViewItem(widgets.StyleOptionMixin, QtWidgets.QStyleOptionViewItem):
    def get_view_item_position(self) -> ViewItemPositionStr:
        return VIEW_ITEM_POSITION.inverse[self.viewItemPosition]

    def get_features(self) -> ViewItemFeatureStr:
        return VIEW_ITEM_FEATURE.get_list(self.features)

    def get_decoration_position(self) -> PositionStr:
        return POSITION.inverse[self.decorationPosition]

    def get_checkstate(self) -> constants.StateStr:
        return constants.STATE.inverse[self.checkState]

    def get_decoration_alignment(self) -> constants.AlignmentStr:
        return constants.ALIGNMENTS.inverse[self.decorationAlignment]


if __name__ == "__main__":
    item = StyleOptionViewItem()
