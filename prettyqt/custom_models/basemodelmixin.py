from typing import Callable

from prettyqt import constants


class BaseModelMixin:

    DATA_ROLE = constants.USER_ROLE
    DTYPE_ROLE = constants.USER_ROLE + 1
    NAME_ROLE = constants.USER_ROLE + 2
    SORT_ROLE = constants.USER_ROLE + 3
    MAX_ROWS = 1_000_000
    HEADER = ["Name"]
    DEFAULT_FLAGS = (
        constants.DRAG_ENABLED
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

    def headerData(self, offset: int, orientation, role):
        if role == constants.DISPLAY_ROLE:
            if orientation == constants.HORIZONTAL:
                return self.HEADER[offset]

    def columnCount(self, parent=None):
        return len(self.HEADER)

    def flags(self, index):
        """Returns corresponding flags for cell of supplied index.

        required override for AbstractitemModels
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
            if fn := self.DECORATIONS.get(index.column()):
                return fn(item)
        elif role in [constants.DISPLAY_ROLE, constants.EDIT_ROLE]:
            if fn := self.LABELS.get(index.column()):
                return fn(item)
        elif role == constants.TOOLTIP_ROLE:
            if fn := self.TOOLTIPS.get(index.column()):
                return fn(item)
        elif role == constants.CHECKSTATE_ROLE:
            if fn := self.CHECKSTATE.get(index.column()):
                return fn(item)
        elif role == self.DATA_ROLE:
            return item
        return None

    def setData(self, index, value, role):
        if role == constants.EDIT_ROLE:
            if not value:
                return False
            item = self.data_by_index(index)
            if fn := self.SET_DATA.get(index.column()):
                fn(item, value)
                self.update_row(index.row())
                return True
