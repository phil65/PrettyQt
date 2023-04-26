from __future__ import annotations

from prettyqt import constants, core, gui
from prettyqt.qt import QtCore, QtGui
from prettyqt.utils import InvalidParamError


class Drag(core.ObjectMixin, QtGui.QDrag):
    def get_pixmap(self) -> gui.Pixmap:
        return gui.Pixmap(self.pixmap())

    def get_default_action(self) -> constants.DropActionStr:
        return constants.DROP_ACTION.inverse[self.defaultAction()]

    def get_drag_cursor(self, action: constants.DropActionStr) -> gui.Pixmap:
        if action not in constants.DROP_ACTION:
            raise InvalidParamError(action, constants.DROP_ACTION)
        px = self.dragCursor(constants.DROP_ACTION[action])
        return gui.Pixmap(px)

    def set_drag_cursor(self, cursor: QtGui.QPixmap, action: constants.DropActionStr):
        self.setDragCursor(cursor, constants.DROP_ACTION[action])

    def get_supported_actions(self) -> list[constants.DropActionStr]:
        return constants.DROP_ACTION.get_list(self.supportedActions())

    def main_loop(
        self,
        supported_actions: list[constants.DropActionStr] | None = None,
        default_drop_action: constants.DropActionStr | None = None,
    ):
        supported_actions = supported_actions or [constants.DROP_ACTION["move"]]
        flag = QtCore.Qt.DropAction(0)
        for i in supported_actions:
            flag |= constants.DROP_ACTION[i]
        default_action = constants.DROP_ACTION[default_drop_action]
        self.exec(flag, default_action)


if __name__ == "__main__":
    obj = core.Object()
    drag = Drag(obj)
    drag.get_pixmap()
