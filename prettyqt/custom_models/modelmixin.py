from typing import Callable

from prettyqt import constants


class ModelMixin:

    DATA_ROLE = constants.USER_ROLE
    DTYPE_ROLE = constants.USER_ROLE + 1  # type: ignore
    NAME_ROLE = constants.USER_ROLE + 2  # type: ignore
    SORT_ROLE = constants.USER_ROLE + 3  # type: ignore
    MAX_ROWS = 1_000_000
    HEADER = ["Name"]
    DEFAULT_FLAGS = (
        constants.DRAG_ENABLED  # type: ignore
        | constants.IS_ENABLED
        | constants.IS_SELECTABLE
        | constants.NO_CHILDREN
    )
    LABELS: dict = dict()
    CHECKSTATE: dict = dict()
    TOOLTIPS: dict = dict()
    DECORATIONS: dict = dict()
    SET_DATA: dict = dict()
    content_type = ""
    data_by_index: Callable
    update_row: Callable

    def headerData(self, offset: int, orientation, role):
        if role == constants.DISPLAY_ROLE:
            if orientation == constants.HORIZONTAL:
                return self.HEADER[offset]

    def columnCount(self, parent=None):
        return len(self.HEADER)

    def flags(self, index):
        """Required override for AbstractitemModels.

        returns corresponding flags for cell of supplied index
        """
        if not index.isValid():
            return constants.DROP_ENABLED
        if index.column() in self.SET_DATA:
            return self.DEFAULT_FLAGS | constants.IS_EDITABLE
        return self.DEFAULT_FLAGS

    def data(self, index, role=constants.DISPLAY_ROLE):
        if not index.isValid():
            return None
        item = self.data_by_index(index)
        if role == constants.DECORATION_ROLE:
            fn = self.DECORATIONS.get(index.column())
            if fn:
                return fn(item)
        elif role in [constants.DISPLAY_ROLE, constants.EDIT_ROLE]:
            fn = self.LABELS.get(index.column())
            if fn:
                return fn(item)
        elif role == constants.TOOLTIP_ROLE:
            fn = self.TOOLTIPS.get(index.column())
            if fn:
                return fn(item)
        elif role == constants.CHECKSTATE_ROLE:
            fn = self.CHECKSTATE.get(index.column())
            if fn:
                return fn(item)
        elif role == self.DATA_ROLE:
            return item
        return None

    def setData(self, index, value, role):
        if role == constants.EDIT_ROLE:
            if not value:
                return False
            item = self.data_by_index(index)
            fn = self.SET_DATA.get(index.column())
            if fn:
                fn(item, value)
                self.update_row(index.row())
                return True
