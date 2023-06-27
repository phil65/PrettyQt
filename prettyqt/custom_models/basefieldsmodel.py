from __future__ import annotations

import contextlib
import logging
from typing import Any

from prettyqt import constants, core

logger = logging.getLogger(__name__)


class BaseFieldsModel(core.AbstractTableModel):
    HEADER: list[str] = []

    def __init__(self, instance, **kwargs):
        self._instance = instance
        self._fields = self.get_fields(instance)
        super().__init__(**kwargs)
        self.set_instance(instance)

    def get_fields(self, instance):
        return NotImplemented

    def set_instance(self, instance):
        self._instance = instance
        self._fields = self.get_fields(instance)
        self.update_all()

    def columnCount(self, parent=None) -> int:
        return len(self.HEADER)

    def headerData(
        self,
        section: int,
        orientation: constants.Orientation,
        role: constants.ItemDataRole = constants.DISPLAY_ROLE,
    ) -> str | None:
        match orientation, role:
            case constants.HORIZONTAL, constants.DISPLAY_ROLE:
                return self.HEADER[section]
            case constants.VERTICAL, constants.DISPLAY_ROLE:
                field = self._fields[section]
                return field.name

    def setData(
        self,
        index: core.ModelIndex,
        value: Any,
        role: constants.ItemDataRole = constants.EDIT_ROLE,
    ) -> bool:
        if not index.isValid():
            return None
        field = self._fields[index.row()]
        match role, index.column():
            case constants.USER_ROLE, _:
                setattr(self._instance, field.name, value)
                self.update_row(index.row())
                return True
        return False

    def rowCount(self, parent: core.ModelIndex | None = None) -> int:
        """Override for AbstractitemModel base method."""
        parent = parent or core.ModelIndex()
        if parent.column() > 0:
            return 0
        return 0 if parent.isValid() else len(self._fields)

    def flags(self, index: core.ModelIndex) -> constants.ItemFlag:
        field = self._fields[index.row()]
        if index.column() == 0:
            val = getattr(self._instance, field.name)
            with contextlib.suppress(Exception):
                setattr(self._instance, field.name, val)
                return super().flags(index) | constants.IS_EDITABLE
        return super().flags(index)
