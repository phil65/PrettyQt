from __future__ import annotations

from typing import Any

from prettyqt import constants, core


class ModelMixin:
    DTYPE_ROLE = constants.USER_ROLE + 1  # type: ignore
    HEADER = ["Name"]
    LABELS: dict = {}
    CHECKSTATE: dict = {}
    TOOLTIPS: dict = {}
    DECORATIONS: dict = {}
    SET_DATA: dict = {}
    content_type = ""

    def headerData(
        self,
        offset: int,
        orientation: constants.Orientation,
        role: constants.ItemDataRole = constants.DISPLAY_ROLE,
    ):
        match orientation, role:
            case constants.HORIZONTAL, constants.DISPLAY_ROLE:
                return self.HEADER[offset]

    def columnCount(self, parent=None):
        return len(self.HEADER)

    def flags(self, index: core.ModelIndex) -> constants.ItemFlag:
        """Override for AbstractitemModel base method.

        returns corresponding flags for cell of supplied index
        """
        if not index.isValid():
            return constants.DROP_ENABLED
        if index.column() in self.SET_DATA:
            return self.DEFAULT_FLAGS | constants.IS_EDITABLE
        return self.DEFAULT_FLAGS

    def data(
        self,
        index: core.ModelIndex,
        role: constants.ItemDataRole = constants.DISPLAY_ROLE,
    ):
        if not index.isValid():
            return None
        item = self.data_by_index(index)
        match role:
            case constants.DECORATION_ROLE:
                if fn := self.DECORATIONS.get(index.column()):
                    return fn(item)
            case constants.DISPLAY_ROLE | constants.EDIT_ROLE:
                if fn := self.LABELS.get(index.column()):
                    return fn(item)
            case constants.TOOLTIP_ROLE:
                if fn := self.TOOLTIPS.get(index.column()):
                    return fn(item)
            case constants.CHECKSTATE_ROLE:
                if fn := self.CHECKSTATE.get(index.column()):
                    return fn(item)
            case constants.USER_ROLE:
                return item
            case _:
                return None

    def setData(
        self,
        index: core.ModelIndex,
        value: Any,
        role: constants.ItemDataRole = constants.EDIT_ROLE,
    ) -> bool:
        if role == constants.EDIT_ROLE:
            if not value:
                return False
            item = self.data_by_index(index)
            if fn := self.SET_DATA.get(index.column()):
                fn(item, value)
                self.update_row(index.row())
                return True
