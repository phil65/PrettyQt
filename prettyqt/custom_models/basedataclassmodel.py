from __future__ import annotations

import collections

from collections.abc import Sequence
import contextlib
import functools
import logging
from operator import and_
from typing import Any

from prettyqt import constants, core


logger = logging.getLogger(__name__)


def lca_type(classes: list[type]) -> type:
    return next(
        iter(functools.reduce(and_, (collections.Counter(cls.mro()) for cls in classes)))
    )


class BaseDataclassModel(core.AbstractTableModel):
    def __init__(self, items: Sequence, **kwargs):
        super().__init__(**kwargs)
        self.items = items
        klasses = [type(i) for i in items]
        self.Class = lca_type(klasses)
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
        match role:
            case constants.DISPLAY_ROLE:
                return repr(getattr(instance, field_name))
            case constants.USER_ROLE | constants.EDIT_ROLE:
                return getattr(instance, field_name)

    def setData(
        self,
        index: core.ModelIndex,
        value: Any,
        role: constants.ItemDataRole = constants.EDIT_ROLE,
    ) -> bool:
        field_name = self._field_names[index.column()]
        instance = self.items[index.row()]
        match role:
            case constants.USER_ROLE:
                with self.reset_model():
                    setattr(instance, field_name, value)
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
        parent = parent or core.ModelIndex()
        field_name = self._field_names[parent.column()]
        instance = self.items[parent.row()]
        # need to cover not parent.isValid()?
        val = getattr(instance, field_name)
        with contextlib.suppress(Exception):
            setattr(instance, field_name, val)
            return super().flags(parent) | constants.IS_EDITABLE
        return super().flags(parent)
