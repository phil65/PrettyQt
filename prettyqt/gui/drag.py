from __future__ import annotations

from prettyqt import constants, core, gui
from prettyqt.qt import QtGui
from prettyqt.utils import InvalidParamError


QtGui.QDrag.__bases__ = (core.Object,)


class Drag(QtGui.QDrag):
    def get_pixmap(self) -> gui.Pixmap:
        return gui.Pixmap(self.pixmap())

    def get_default_action(self) -> constants.DropActionStr:
        return constants.DROP_ACTION.inverse[self.defaultAction()]

    def get_drag_cursor(self, action: constants.DropActionStr) -> gui.Pixmap:
        if action not in constants.DROP_ACTION:
            raise InvalidParamError(action, constants.DROP_ACTION)
        px = self.dragCursor(constants.DROP_ACTION[action])
        return gui.Pixmap(px)

    def get_supported_actions(self) -> list[constants.DropActionStr]:
        return [
            k for k, v in constants.DROP_ACTION.items() if v & self.supportedActions()
        ]


if __name__ == "__main__":
    obj = core.Object()
    drag = Drag(obj)
    drag.get_pixmap()
