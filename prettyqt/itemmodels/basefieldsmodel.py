from __future__ import annotations

import dataclasses
import logging
from typing import TYPE_CHECKING, Any, ClassVar

from prettyqt import constants, core, gui


if TYPE_CHECKING:
    from collections.abc import Mapping


logger = logging.getLogger(__name__)


class BaseFieldsModel(core.AbstractTableModel):
    """Base table model showing the fields of a single dataclass-like instance.

    Each row is a field (field name in the vertical header), column 0 contains the
    (editable) value, the other columns contain field metadata.
    """

    HEADER: ClassVar[list[str]] = []
    DELEGATE_DEFAULT = "editor"

    def __init__(self, instance, **kwargs):
        super().__init__(**kwargs)
        self._instance = instance
        self._fields = self.get_fields(instance)
        self._field_names = list(self._fields.keys())

    def get_fields(self, instance) -> Mapping[str, Any]:
        raise NotImplementedError

    def set_instance(self, instance):
        with self.reset_model():
            self._instance = instance
            self._fields = self.get_fields(instance)
            self._field_names = list(self._fields.keys())

    def columnCount(self, parent: core.ModelIndex | None = None) -> int:
        parent = parent or core.ModelIndex()
        return 0 if parent.isValid() else len(self.HEADER)

    def headerData(
        self,
        section: int,
        orientation: constants.Orientation,
        role: constants.ItemDataRole = constants.DISPLAY_ROLE,
    ) -> str | None:
        match orientation, role:
            case constants.HORIZONTAL, constants.DISPLAY_ROLE if section < len(
                self.HEADER
            ):
                return self.HEADER[section]
            case constants.VERTICAL, constants.DISPLAY_ROLE if section < len(
                self._field_names
            ):
                return self._field_names[section]
        return None

    @staticmethod
    def _to_display(value: Any) -> str:
        """Display text for metadata values (types, defaults, ...)."""
        if value is None or value is dataclasses.MISSING or repr(value) in _MISSING_REPRS:
            return ""
        if isinstance(value, type):
            return value.__name__
        return value if isinstance(value, str) else repr(value)

    def _get_value_data(self, value: Any, role: constants.ItemDataRole):
        """Data for the value column (column 0)."""
        match role:
            case constants.DISPLAY_ROLE if not isinstance(value, bool):
                return repr(value)
            case constants.CHECKSTATE_ROLE if isinstance(value, bool):
                return self.to_checkstate(value)
            case constants.EDIT_ROLE | constants.USER_ROLE:
                return value
            case constants.FONT_ROLE:
                font = gui.QFont()
                font.setBold(True)
                return font
        return None

    def setData(
        self,
        index: core.ModelIndex,
        value: Any,
        role: constants.ItemDataRole = constants.EDIT_ROLE,
    ) -> bool:
        if not index.isValid() or index.column() != 0:
            return False
        field_name = self._field_names[index.row()]
        match role:
            case constants.USER_ROLE | constants.EDIT_ROLE:
                pass
            case constants.CHECKSTATE_ROLE:
                value = self.from_checkstate(value)
            case _:
                return False
        try:
            setattr(self._instance, field_name, value)
        except Exception:
            logger.exception("Could not set %s to %r", field_name, value)
            return False
        self.update_row(index.row())
        return True

    def rowCount(self, parent: core.ModelIndex | None = None) -> int:
        """Override for AbstractitemModel base method."""
        parent = parent or core.ModelIndex()
        return 0 if parent.isValid() else len(self._field_names)

    def _is_writable(self, field_name: str) -> bool:
        """Dumb check, set same value and check if it works.

        Should be overridden by subclasses if possible.
        """
        val = getattr(self._instance, field_name)
        try:
            setattr(self._instance, field_name, val)
        except Exception:  # noqa: BLE001
            return False
        return True

    def flags(self, index: core.ModelIndex) -> constants.ItemFlag:
        flags = super().flags(index)
        if not index.isValid() or index.column() != 0:
            return flags
        field_name = self._field_names[index.row()]
        if not self._is_writable(field_name):
            return flags
        if isinstance(getattr(self._instance, field_name), bool):
            return flags | constants.IS_CHECKABLE
        return flags | constants.IS_EDITABLE


# reprs of the "no default" sentinels of attrs and pydantic
_MISSING_REPRS = {"NOTHING", "PydanticUndefined"}
