from __future__ import annotations

import contextlib

from prettyqt import constants
from prettyqt.qt import QtGui


class UserData(QtGui.QTextBlockUserData):
    def __init__(self, data):
        super().__init__()
        self.data = data

    def __repr__(self):
        return f"{type(self).__name__}({repr(self.data)})"


class TextBlock(QtGui.QTextBlock):
    def __repr__(self):
        return f"{type(self).__name__}({self.text()!r})"

    def __contains__(self, position: int):
        return self.contains(position)

    def __bool__(self):
        return self.isValid()

    def __str__(self):
        return self.text()

    def get_previous(self) -> TextBlock:
        return TextBlock(self.previous())

    def get_next(self) -> TextBlock:
        return TextBlock(self.next())

    def get_text_direction(self) -> constants.LayoutDirectionStr:
        return constants.LAYOUT_DIRECTION.inv[self.textDirection()]

    def set_user_data(self, data):
        if isinstance(data, QtGui.QTextBlockUserData):
            self.setUserData(data)
            return None
        user_data = UserData(data)
        self.setUserData(user_data)

    def get_user_data(self):
        user_data = self.userData()
        if isinstance(user_data, UserData):
            print(user_data.data)
            return user_data.data
        return user_data

    @contextlib.contextmanager
    def edit_user_state(self):
        state = self.userState()
        yield state
        self.setUserState(state)

    def get_state(self) -> int:
        """Get the user state, generally used for syntax highlighting.

        :return: The block state
        """
        state = self.userState()
        if state == -1:
            return state
        return state & 0x0000FFFF

    def set_state(self, state: int):
        """Set the user state, generally used for syntax highlighting.

        :param state: new state value.
        """
        user_state = self.userState()
        if user_state == -1:
            user_state = 0
        higher_part = user_state & 0x7FFF0000
        state &= 0x0000FFFF
        state |= higher_part
        self.setUserState(state)

    def get_fold_level(self) -> int:
        """Get the block fold level.

        :return: The block fold level
        """
        state = self.userState()
        if state == -1:
            state = 0
        return (state & 0x03FF0000) >> 16

    def set_fold_level(self, val: int):
        """Set the block fold level.

        :param val: The new fold level [0-7]
        """
        state = self.userState()
        if state == -1:
            state = 0
        if val >= 0x3FF:
            val = 0x3FF
        state &= 0x7C00FFFF
        state |= val << 16
        self.setUserState(state)

    def is_fold_trigger(self) -> bool:
        """Check if the block is a fold trigger.

        :return: True if the block is a fold trigger (represented as a node in
            the fold panel)
        """
        state = self.userState()
        if state == -1:
            state = 0
        return bool(state & 0x04000000)

    def set_fold_trigger(self, val: int):
        """Set the block fold trigger flag (True means the block is a fold trigger).

        :param val: value to set
        """
        state = self.userState()
        if state == -1:
            state = 0
        state &= 0x7BFFFFFF
        state |= int(val) << 26
        self.setUserState(state)

    def is_collapsed(self) -> bool:
        """Check if the block is expanded or collased.

        :return: False for an open trigger, True for for closed trigger
        """
        state = self.userState()
        if state == -1:
            state = 0
        return bool(state & 0x08000000)

    def set_collapsed(self, val: int):
        """Set the fold trigger state (collapsed or expanded).

        :param val: The new trigger state (True=collapsed, False=expanded)
        """
        state = self.userState()
        if state == -1:
            state = 0
        state &= 0x77FFFFFF
        state |= int(val) << 27
        self.setUserState(state)

    def find_parent_scope(self, limit: int = 5000) -> TextBlock | None:
        """Find parent scope, if the block is not a fold trigger."""
        # if we moved up for more than n lines, just give up otherwise this
        # would take too much time.
        counter = 0
        original = TextBlock(self)
        start = TextBlock(self)
        if not self.is_fold_trigger():
            # search level of next non blank line
            while start.text().strip() == "" and start.isValid():
                start = start.next()
            ref_level = self.get_fold_level() - 1
            start = original
            while (
                start.blockNumber()
                and counter < limit
                and (not self.is_fold_trigger() or self.get_fold_level() > ref_level)
            ):
                counter += 1
                start = start.previous()
        if counter < limit:
            return TextBlock(start)
        return None


if __name__ == "__main__":
    from prettyqt import gui

    doc = gui.TextDocument()
    doc.set_text("a\nb\ncd")
    block = doc[0]
    block.set_user_data("testg")
    print(block.get_user_data())
