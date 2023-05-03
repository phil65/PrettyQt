# credits to SuperQt (https://github.com/pyapp-kit/superqt)

from __future__ import annotations

import enum
from typing import TypeVar

from prettyqt import core, widgets
from prettyqt.qt import QtWidgets
from prettyqt.utils import get_repr


EnumType = TypeVar("EnumType", bound=enum.Enum)


NONE_STRING = "----"


def _get_name(enum_value: enum.Enum):
    """Create human readable name if user does not implement `__str__`."""
    if (
        enum_value.__str__.__module__ != "enum"
        and not enum_value.__str__.__module__.startswith("shibokensupport")
    ):
        # check if function was overloaded
        return str(enum_value)
    else:
        return enum_value.name.replace("_", " ")


class EnumComboBox(widgets.ComboBox):
    """ComboBox presenting options from a python Enum.

    If the Enum class does not implement `__str__` then a human readable name
    is created from the name of the enum member, replacing underscores with spaces.
    """

    # current_enum_changed = core.Signal(object)

    def __init__(
        self,
        parent: QtWidgets.QWidget | None = None,
        enum_class: enum.EnumMeta | None = None,
        allow_none: bool = False,
    ):
        super().__init__(parent)
        self._enum_class = None
        self._allow_none = False
        if enum_class is not None:
            self.set_enum_class(enum_class, allow_none)
        # self.currentIndexChanged.connect(self._emit_signal)

    def __repr__(self):
        return get_repr(self, enum_class=self._enum_class, allow_none=self._allow_none)

    def set_enum_class(self, enum: enum.EnumMeta | None, allow_none: bool = False):
        """Set enum class from which members value should be selected."""
        self.clear()
        self._enum_class = enum
        self._allow_none = allow_none and enum is not None
        if allow_none:
            super().addItem(NONE_STRING)
        items = [_get_name(i) for i in self._enum_class.__members__.values()]
        super().addItems(items)

    def get_enum_class(self) -> enum.EnumMeta | None:
        """Return current Enum class."""
        return self._enum_class

    def is_optional(self) -> bool:
        """Return if current enum is with optional annotation."""
        return self._allow_none

    def clear(self):
        self._enum_class = None
        self._allow_none = False
        super().clear()

    def get_value(self) -> EnumType | None:
        """Current value as Enum member."""
        if self._enum_class is None:
            return None
        class_members = list(self._enum_class.__members__.values())
        if not self._allow_none:
            return class_members[self.currentIndex()]
        is_none = self.currentText() == NONE_STRING
        return None if is_none else class_members[self.currentIndex() - 1]

    def set_value(self, value: EnumType | None) -> None:
        """Set value with Enum."""
        if self._enum_class is None:
            raise RuntimeError("Uninitialized enum class. Use `set_enum_class` first.")
        if value is None and self._allow_none:
            self.setCurrentIndex(0)
            return
        if not isinstance(value, self._enum_class):
            raise TypeError(
                "setValue(self, Enum): argument 1 has unexpected type "
                f"{type(value).__name__!r}"
            )
        self.setCurrentText(_get_name(value))

    # def _emit_signal(self):
    #     if self._enum_class is not None:
    #         self.current_enum_changed.emit(self.get_value())

    def insertItems(self, *_, **__):
        raise RuntimeError("EnumComboBox does not allow to insert items")

    def insertItem(self, *_, **__):
        raise RuntimeError("EnumComboBox does not allow to insert item")

    def addItems(self, *_, **__):
        raise RuntimeError("EnumComboBox does not allow to add items")

    def addItem(self, *_, **__):
        raise RuntimeError("EnumComboBox does not allow to add item")

    def setInsertPolicy(self, policy):
        raise RuntimeError("EnumComboBox does not allow to insert item")

    enum_value = core.Property(enum.Enum, get_value, set_value, user=True)


if __name__ == "__main__":
    from prettyqt.qt import QtCore

    app = widgets.app()
    cb = EnumComboBox()
    cb.set_enum_class(QtCore.Qt.ItemDataRole)
    cb.set_value(QtCore.Qt.ItemDataRole.EditRole)
    cb.show()
    cb.value_changed.connect(print)
    app.main_loop()
