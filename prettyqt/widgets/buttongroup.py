from __future__ import annotations

from prettyqt.qt import QtWidgets
from prettyqt import core


class ButtonGroup(core.ObjectMixin, QtWidgets.QButtonGroup):
    def serialize_fields(self):
        return dict(exclusive=self.exclusive())

    def __getitem__(self, index: int) -> QtWidgets.QAbstractButton:
        return self.button(index)
