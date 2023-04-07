from __future__ import annotations

from prettyqt import widgets
from prettyqt.qt import QtWidgets


class StyledItemDelegate(
    widgets.AbstractItemDelegateMixin, QtWidgets.QStyledItemDelegate
):
    pass
