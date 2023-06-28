from __future__ import annotations

from typing import Literal

from prettyqt import constants, widgets
from prettyqt.utils import bidict


PositionStr = Literal["left", "right", "top", "bottom"]

POSITION: bidict[PositionStr, widgets.QStyleOptionViewItem.Position] = bidict(
    left=widgets.QStyleOptionViewItem.Position.Left,
    right=widgets.QStyleOptionViewItem.Position.Right,
    top=widgets.QStyleOptionViewItem.Position.Top,
    bottom=widgets.QStyleOptionViewItem.Position.Bottom,
)

ViewItemFeatureStr = Literal[
    "none",
    "wrap_text",
    "alternate",
    "has_check_indicator",
    "has_display",
    "has_decoration",
]

VIEW_ITEM_FEATURE: bidict[ViewItemFeatureStr, widgets.QStyleOptionViewItem] = bidict(
    none=widgets.QStyleOptionViewItem.ViewItemFeature(0),  # type: ignore
    wrap_text=widgets.QStyleOptionViewItem.ViewItemFeature.WrapText,
    alternate=widgets.QStyleOptionViewItem.ViewItemFeature.Alternate,
    has_check_indicator=widgets.QStyleOptionViewItem.ViewItemFeature.HasCheckIndicator,
    has_display=widgets.QStyleOptionViewItem.ViewItemFeature.HasDisplay,
    has_decoration=widgets.QStyleOptionViewItem.ViewItemFeature.HasDecoration,
)


ViewItemPositionStr = Literal["invalid", "beginning", "middle", "end", "only_one"]

VIEW_ITEM_POSITION: bidict[
    ViewItemPositionStr, widgets.QStyleOptionViewItem.ViewItemPosition
] = bidict(
    invalid=widgets.QStyleOptionViewItem.ViewItemPosition.Invalid,
    beginning=widgets.QStyleOptionViewItem.ViewItemPosition.Beginning,
    middle=widgets.QStyleOptionViewItem.ViewItemPosition.Middle,
    end=widgets.QStyleOptionViewItem.ViewItemPosition.End,
    only_one=widgets.QStyleOptionViewItem.ViewItemPosition.OnlyOne,
)


class StyleOptionViewItem(widgets.StyleOptionMixin, widgets.QStyleOptionViewItem):
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
