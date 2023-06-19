from __future__ import annotations

from collections.abc import Sequence
import collections
import functools
import contextlib
import logging
from operator import and_
from typing import Any

from prettyqt import constants, core
from prettyqt.qt import QtCore

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
        self.fields = self.get_fields()
        self.fields.sort(key=lambda x: x.name)

    def get_fields(self):
        return NotImplemented

    def columnCount(self, parent=None):
        return len(self.fields)

    def headerData(
        self,
        section: int,
        orientation: QtCore.Qt.Orientation,
        role: QtCore.Qt.ItemDataRole = constants.DISPLAY_ROLE,
    ) -> str | None:
        match orientation, role, section:
            case constants.VERTICAL, constants.DISPLAY_ROLE, _:
                instance = self.items[section]
                return type(instance).__name__
            case constants.HORIZONTAL, constants.DISPLAY_ROLE, _:
                return self.fields[section].name

    def data(self, index: core.ModelIndex, role=constants.DISPLAY_ROLE):
        if not index.isValid():
            return None
        field = self.fields[index.column()]
        instance = self.items[index.row()]
        match role:
            case constants.DISPLAY_ROLE | constants.EDIT_ROLE:
                return repr(getattr(instance, field.name))
            case constants.USER_ROLE:
                return getattr(instance, field.name)

    def setData(
        self,
        index: core.ModelIndex,
        value: Any,
        role: constants.ItemDataRole = constants.EDIT_ROLE,
    ) -> bool:
        field = self.fields[index.column()]
        instance = self.items[index.row()]
        match role:
            case constants.USER_ROLE:
                with self.reset_model():
                    setattr(instance, field.name, value)
                return True
        return False

    def rowCount(self, parent=None):
        """Override for AbstractitemModel base method."""
        parent = parent or core.ModelIndex()
        if parent.column() > 0:
            return 0
        return 0 if parent.isValid() else len(self.items)

    def flags(self, parent=None):
        """Override.

        BaseClass implementation just tries to set attribute with same value to test
        if field is writable. If possible, subclasses should find a more efficient way.
        """
        if not parent.isValid():
            return super().flags(parent)
        parent = parent or core.ModelIndex()
        field = self.fields[parent.column()]
        instance = self.items[parent.row()]
        # need to cover not parent.isValid()?
        val = getattr(instance, field.name)
        with contextlib.suppress(Exception):
            setattr(instance, field.name, val)
            return super().flags(parent) | constants.IS_EDITABLE
        return super().flags(parent)
