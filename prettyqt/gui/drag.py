from __future__ import annotations

from typing import TYPE_CHECKING

from prettyqt import constants, core, gui


if TYPE_CHECKING:
    from collections.abc import Iterable


class Drag(core.ObjectMixin, gui.QDrag):
    """Support for MIME-based drag and drop data transfer."""

    def get_pixmap(self) -> gui.Pixmap:
        return gui.Pixmap(self.pixmap())

    def get_default_action(self) -> constants.DropActionStr:
        return constants.DROP_ACTION.inverse[self.defaultAction()]

    def get_drag_cursor(
        self, action: constants.DropActionStr | constants.DropAction
    ) -> gui.Pixmap:
        px = self.dragCursor(constants.DROP_ACTION.get_enum_value(action))
        return gui.Pixmap(px)

    def set_drag_cursor(
        self,
        cursor: gui.QPixmap,
        action: constants.DropActionStr | constants.DropAction,
    ):
        self.setDragCursor(cursor, constants.DROP_ACTION.get_enum_value(action))

    def get_supported_actions(self) -> list[constants.DropActionStr]:
        return constants.DROP_ACTION.get_list(self.supportedActions())

    def main_loop(
        self,
        supported_actions: Iterable[constants.DropActionStr | constants.DropAction]
        | None = None,
        default_drop_action: constants.DropActionStr | constants.DropAction | None = None,
    ) -> constants.DropActionStr:
        supported_actions = supported_actions or [constants.DROP_ACTION["move"]]
        flag = constants.DropAction(0)
        for i in supported_actions:
            flag |= constants.DROP_ACTION.get_enum_value(i)
        default_action = constants.DROP_ACTION.get_enum_value(default_drop_action)
        result = super().exec(flag, default_action)
        return constants.DROP_ACTION.inverse[result]


if __name__ == "__main__":
    obj = core.Object()
    drag = Drag(obj)
    drag.get_pixmap()
