from __future__ import annotations

from prettyqt import core
from prettyqt.qt import QtWidgets


class ButtonGroup(core.ObjectMixin, QtWidgets.QButtonGroup):
    """Container to organize groups of button widgets."""

    def __getitem__(self, index: int) -> QtWidgets.QAbstractButton:
        return self.button(index)
