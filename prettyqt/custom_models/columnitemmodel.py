from typing import Optional, List
import logging

from qtpy import QtWidgets

from prettyqt import core, constants
from prettyqt.utils import columnitem

logger = logging.getLogger(__name__)


class ColumnItemModel(core.AbstractItemModel):
    """Model that provides an interface to an objectree that is build of TreeItems."""

    def __init__(
        self,
        attr_cols: Optional[List[columnitem.ColumnItem]] = None,
        parent: Optional[QtWidgets.QWidget] = None,
    ):
        super().__init__(parent)
        self._attr_cols = attr_cols

    def columnCount(self, _parent=None):
        """Return the number of columns in the tree."""
        return len(self._attr_cols)

    def data(self, index, role):
        """Return the tree item at the given index and role."""
        if not index.isValid():
            return None

        col = index.column()
        tree_item = index.internalPointer()

        if role in [constants.DISPLAY_ROLE, constants.EDIT_ROLE]:
            func = self._attr_cols[col].label
            if func is None:
                return ""
            attr = func(tree_item)
            return attr.replace("\n", " ")
        elif role == constants.DECORATION_ROLE:
            return self._attr_cols[col].get_decoration(tree_item)
        elif role == constants.CHECKSTATE_ROLE:
            return self._attr_cols[col].get_checkstate(tree_item)
        elif role == constants.ALIGNMENT_ROLE:
            return self._attr_cols[col].get_alignment(tree_item)
        elif role == constants.FOREGROUND_ROLE:
            return self._attr_cols[col].get_foreground_color(tree_item)
        elif role == constants.BACKGROUND_ROLE:
            return self._attr_cols[col].get_background_color(tree_item)
        elif role == constants.FONT_ROLE:
            return self._attr_cols[col].get_font(tree_item)
        else:
            return None

    def flags(self, index):
        if not index.isValid():
            return constants.NO_CHILDREN
        return constants.IS_ENABLED | constants.IS_SELECTABLE

    def headerData(self, section, orientation, role):
        if orientation == constants.HORIZONTAL and role == constants.DISPLAY_ROLE:
            return self._attr_cols[section].name
        else:
            return None
