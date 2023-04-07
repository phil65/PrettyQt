from __future__ import annotations

from prettyqt import widgets
from prettyqt.qt import QtWidgets


class StyleOptionComboBox(
    widgets.StyleOptionComplexMixin, QtWidgets.QStyleOptionComboBox
):
    pass
