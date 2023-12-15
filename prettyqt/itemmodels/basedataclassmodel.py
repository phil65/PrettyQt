from __future__ import annotations

from collections.abc import Sequence
import contextlib
import logging
from typing import Any

from prettyqt import constants, core
from prettyqt.utils import classhelpers


logger = logging.getLogger(__name__)


class BaseDataclassModel(core.AbstractTableModel):
    DELEGATE_DEFAULT = "editor"

    def __init__(self, items: Sequence, **kwargs):
        super().__init__(**kwargs)
        self.items = items
        klasses = [type(i) for i in items]
        self.Class = classhelpers.lca_type(klasses)
        logger.debug(f"{type(self).__name__}: found common ancestor {self.Class}")
        self._fields = self.get_fields()
        self._field_names = list(self._fields.keys())

    def get_fields(self):
        return NotImplemented

    def columnCount(self, parent=None):
        return len(self._fields)

    def headerData(
        self,
        section: int,
        orientation: constants.Orientation,
        role: constants.ItemDataRole = constants.DISPLAY_ROLE,
    ) -> str | None:
        match orientation, role, section:
            case constants.VERTICAL, constants.DISPLAY_ROLE, _:
                instance = self.items[section]
                return type(instance).__name__
            case constants.HORIZONTAL, constants.DISPLAY_ROLE, _:
                return self._field_names[section]

    def data(
        self,
        index: core.ModelIndex,
        role: constants.ItemDataRole = constants.DISPLAY_ROLE,
    ):
        if not index.isValid():
            return None
        field_name = self._field_names[index.column()]
        instance = self.items[index.row()]
        value = getattr(instance, field_name)
        match role:
            case constants.DISPLAY_ROLE if not isinstance(value, bool):
                return repr(value)
            case constants.CHECKSTATE_ROLE if isinstance(value, bool):
                return self.to_checkstate(value)
            case constants.USER_ROLE | constants.EDIT_ROLE:
                return value

    def setData(
        self,
        index: core.ModelIndex,
        value: Any,
        role: constants.ItemDataRole = constants.EDIT_ROLE,
    ) -> bool:
        field_name = self._field_names[index.column()]
        instance = self.items[index.row()]
        match role:
            case constants.EDIT_ROLE | constants.USER_ROLE:
                with self.reset_model():
                    setattr(instance, field_name, value)
                return True
            case constants.CHECKSTATE_ROLE:
                with self.reset_model():
                    setattr(instance, field_name, bool(value))
                return True
        return False

    def rowCount(self, parent: core.ModelIndex | None = None) -> int:
        """Override for AbstractitemModel base method."""
        parent = parent or core.ModelIndex()
        if parent.column() > 0:
            return 0
        return 0 if parent.isValid() else len(self.items)

    def flags(self, parent: core.ModelIndex) -> constants.ItemFlag:
        """Override.

        BaseClass implementation just tries to set attribute with same value to test
        if field is writable. If possible, subclasses should find a more efficient way.
        """
        if not parent.isValid():
            return super().flags(parent)
        field_name = self._field_names[parent.column()]
        instance = self.items[parent.row()]
        # need to cover not parent.isValid()?
        val = getattr(instance, field_name)
        with contextlib.suppress(Exception):
            setattr(instance, field_name, val)
            if isinstance(val, bool):
                return super().flags(parent) | constants.IS_CHECKABLE
            else:
                return super().flags(parent) | constants.IS_EDITABLE
        return super().flags(parent)
