# -*- coding: utf-8 -*-
"""
@author: Philipp Temminghoff
"""

from typing import Dict

from prettyqt import constants


class SelectionMixin(object):

    CHECKSTATE: Dict = {}  # column: identifier

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.selected = dict()

    def setData(self, index, value, role):
        if not index.isValid():
            return False
        elif role == constants.CHECKSTATE_ROLE:
            name = self._get_selection_id(index)
            self.selected[name] = not self.selected[name]
            self.dataChanged.emit(index, index)
            return True
        return super().setData(index, value, role)

    def data(self, index, role=constants.DISPLAY_ROLE):
        if not index.isValid():
            return False
        if role == constants.CHECKSTATE_ROLE:
            if index.column() == 0:
                name = self._get_selection_id(index)
                selected = self.selected.get(name, False)
                if name not in self.selected:
                    self.selected[name] = selected
                return selected
        return super().data(index, role)

    def flags(self, index):
        flags = super().flags(index)
        if index.column() in self.CHECKSTATE:
            return flags | constants.IS_CHECKABLE
        return flags

    def _get_selection_id(self, index):
        item = index.data(self.DATA_ROLE)
        id_fn = self.CHECKSTATE.get(index.column())
        if id_fn:
            return id_fn(item)
