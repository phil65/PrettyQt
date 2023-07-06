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
        self._field_names = list(self._fields.keys())
        super().__init__(**kwargs)
        self.set_instance(instance)

    def get_fields(self, instance) -> dict[str, Any]:
        return NotImplemented

    def set_instance(self, instance):
        self._instance = instance
        self._fields = self.get_fields(instance)
        self._field_names = list(self._fields.keys())
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
                return self._field_names[section]

    def setData(
        self,
        index: core.ModelIndex,
        value: Any,
        role: constants.ItemDataRole = constants.EDIT_ROLE,
    ) -> bool:
        if not index.isValid():
            return None
        match role, index.column():
            case constants.USER_ROLE | constants.EDIT_ROLE, _:
                field_name = self._field_names[index.row()]
                setattr(self._instance, field_name, value)
                self.update_row(index.row())
                return True
        return False

    def rowCount(self, parent: core.ModelIndex | None = None) -> int:
        """Override for AbstractitemModel base method."""
        parent = parent or core.ModelIndex()
        if parent.column() > 0:
            return 0
        return 0 if parent.isValid() else len(self._field_names)

    def _is_writable(self, field_name: str) -> bool:
        """Dumb check, set same value and check if it works.

        Should be overridden by subclasses if possible.
        """
        val = getattr(self._instance, field_name)
        with contextlib.suppress(Exception):
            setattr(self._instance, field_name, val)
            return True
        return False

    def flags(self, index: core.ModelIndex) -> constants.ItemFlag:
        field_name = self._field_names[index.row()]
        if index.column() == 0:
            if self._is_writable(field_name):
                return super().flags(index) | constants.IS_EDITABLE
        return super().flags(index)
