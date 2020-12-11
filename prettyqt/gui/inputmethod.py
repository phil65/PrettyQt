from qtpy import QtGui, QtCore

from prettyqt import core
from prettyqt.utils import bidict

ACTION = bidict(
    click=QtGui.QInputMethod.Click, context_menu=QtGui.QInputMethod.ContextMenu
)

LAYOUT_DIRECTION = bidict(
    left_to_right=QtCore.Qt.LeftToRight,
    right_to_left=QtCore.Qt.RightToLeft,
    auto=QtCore.Qt.LayoutDirectionAuto,
)

QtGui.QInputMethod.__bases__ = (core.Object,)


class InputMethod:
    def __init__(self, item: QtGui.QInputMethod):
        self.item = item

    def __getattr__(self, val):
        return getattr(self.item, val)

    def get_anchor_rectangle(self) -> core.RectF:
        return core.RectF(self.anchorRectangle())

    def get_cursor_rectangle(self) -> core.RectF:
        return core.RectF(self.cursorRectangle())

    def get_input_item_clip_rectangle(self) -> core.RectF:
        return core.RectF(self.inputItemClipRectangle())

    def get_input_item_rectangle(self) -> core.RectF:
        return core.RectF(self.inputItemRectangle())

    def get_keyboard_rectangle(self) -> core.RectF:
        return core.RectF(self.keyboardRectangle())

    def get_locale(self) -> core.Locale:
        return core.Locale(self.locale())

    def get_input_direction(self) -> str:
        return LAYOUT_DIRECTION.inverse[self.inputDirection()]


if __name__ == "__main__":
    from prettyqt import gui

    app = gui.app()
    method = app.get_input_method()
