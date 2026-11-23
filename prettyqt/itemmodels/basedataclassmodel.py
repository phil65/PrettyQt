from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any

from prettyqt import constants, core
from prettyqt.utils import classhelpers


if TYPE_CHECKING:
    from collections.abc import Mapping, Sequence


logger = logging.getLogger(__name__)


class BaseDataclassModel(core.AbstractTableModel):
    """Base table model for a list of dataclass-like instances.

    Rows are the instances, columns are the fields of their closest common ancestor.
    Subclasses need to implement `get_fields` and should implement `_is_frozen`.
    """

    DELEGATE_DEFAULT = "editor"

    def __init__(self, items: Sequence, **kwargs):
        super().__init__(**kwargs)
        self.items = items
        self.Class = classhelpers.lca_type([type(i) for i in items]) if items else None
        logger.debug("%s: found common ancestor %s", type(self).__name__, self.Class)
        self._fields = self.get_fields() if self.Class is not None else {}
        self._field_names = list(self._fields.keys())

    def get_fields(self) -> Mapping[str, Any]:
        raise NotImplementedError

    def _is_frozen(self) -> bool | None:
        """Return whether the common class is frozen. None means "unknown"."""
        return None

    def columnCount(self, parent: core.ModelIndex | None = None) -> int:
        parent = parent or core.ModelIndex()
        return 0 if parent.isValid() else len(self._fields)

    def headerData(
        self,
        section: int,
        orientation: constants.Orientation,
        role: constants.ItemDataRole = constants.DISPLAY_ROLE,
    ) -> str | None:
        match orientation, role:
            case constants.VERTICAL, constants.DISPLAY_ROLE if section < len(self.items):
                return type(self.items[section]).__name__
            case constants.HORIZONTAL, constants.DISPLAY_ROLE if section < len(
                self._field_names
            ):
                return self._field_names[section]
        return None

    def _get_value(self, index: core.ModelIndex) -> tuple[Any, str, Any]:
        field_name = self._field_names[index.column()]
        instance = self.items[index.row()]
        return instance, field_name, getattr(instance, field_name)

    def data(
        self,
        index: core.ModelIndex,
        role: constants.ItemDataRole = constants.DISPLAY_ROLE,
    ):
        if not index.isValid():
            return None
        _instance, _field_name, value = self._get_value(index)
        match role:
            case constants.DISPLAY_ROLE if not isinstance(value, bool):
                return repr(value)
            case constants.CHECKSTATE_ROLE if isinstance(value, bool):
                return self.to_checkstate(value)
            case constants.USER_ROLE | constants.EDIT_ROLE:
                return value
        return None

    def setData(
        self,
        index: core.ModelIndex,
        value: Any,
        role: constants.ItemDataRole = constants.EDIT_ROLE,
    ) -> bool:
        if not index.isValid():
            return False
        instance, field_name, _ = self._get_value(index)
        match role:
            case constants.EDIT_ROLE | constants.USER_ROLE:
                pass
            case constants.CHECKSTATE_ROLE:
                value = self.from_checkstate(value)
            case _:
                return False
        try:
            setattr(instance, field_name, value)
        except Exception:
            logger.exception("Could not set %s to %r", field_name, value)
            return False
        self.dataChanged.emit(index, index)
        return True

    def rowCount(self, parent: core.ModelIndex | None = None) -> int:
        """Override for AbstractitemModel base method."""
        parent = parent or core.ModelIndex()
        return 0 if parent.isValid() else len(self.items)

    def _is_writable(self, instance, field_name: str, value) -> bool:
        match self._is_frozen():
            case True:
                return False
            case False:
                return True
        # Unknown: try to set the same value again.
        try:
            setattr(instance, field_name, value)
        except Exception:  # noqa: BLE001
            return False
        return True

    def flags(self, index: core.ModelIndex) -> constants.ItemFlag:
        flags = super().flags(index)
        if not index.isValid():
            return flags
        instance, field_name, value = self._get_value(index)
        if not self._is_writable(instance, field_name, value):
            return flags
        if isinstance(value, bool):
            return flags | constants.IS_CHECKABLE
        return flags | constants.IS_EDITABLE
