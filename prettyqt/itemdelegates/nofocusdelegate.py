from __future__ import annotations

from typing import TYPE_CHECKING

from prettyqt import widgets


if TYPE_CHECKING:
    from prettyqt import core, gui


# https://stackoverflow.com/a/55252650/3620725


class NoFocusDelegate(widgets.StyledItemDelegate):
    """Delegate to remove dotted border on cell focus."""

    ID = "no_focus"

    def paint(
        self,
        painter: gui.QPainter,
        option: widgets.QStyleOptionViewItem,
        index: core.ModelIndex,
    ):
        if option.state & widgets.Style.StateFlag.State_HasFocus:
            option.state = option.state ^ widgets.Style.StateFlag.State_HasFocus
        super().paint(painter, option, index)
