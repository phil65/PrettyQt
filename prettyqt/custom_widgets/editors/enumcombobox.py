# credits to SuperQt (https://github.com/pyapp-kit/superqt)

from __future__ import annotations

import enum
from typing import TypeVar

from prettyqt import core, widgets
from prettyqt.utils import get_repr


EnumType = TypeVar("EnumType", bound=enum.Enum)


NONE_STRING = "----"


class EnumComboBox(widgets.ComboBox):
    """ComboBox presenting options from a python Enum.

    If the Enum class does not implement `__str__` then a human readable name
    is created from the name of the enum member, replacing underscores with spaces.
    """

    # current_enum_changed = core.Signal(object)
    value_changed = core.Signal(enum.Enum)

    def __init__(self, value=None, object_name: str = "enum_combobox", **kwargs):
        self._enum_class = None
        self._allow_none = False
        super().__init__(object_name=object_name, **kwargs)
        if value is not None:
            self.set_value(value)
        # self.currentIndexChanged.connect(self._emit_signal)

    def __repr__(self):
        return get_repr(self, self.get_value())

    def set_allow_none(self, value: bool):
        self._allow_none = value

    def is_none_allowed(self) -> bool:
        return self._allow_none

    def _set_enum_class(self, enum: enum.EnumMeta | None):
        """Set enum class from which members value should be selected."""
        if enum == self._enum_class:
            return
        self._enum_class = enum
        super().clear()
        if self._allow_none and enum is not None:
            super().addItem(NONE_STRING)
        items = [i.name.replace("_", " ") for i in self._enum_class.__members__.values()]
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
        if value is None:
            if not self._allow_none:
                raise ValueError(value)
            self.setCurrentIndex(0)
            return
        if not isinstance(value, enum.Enum):
            value = self._enum_class(value)
        self._set_enum_class(value.__class__)
        self.setCurrentText(value.name.replace("_", " "))

    # def _emit_signal(self):
    #     if self._enum_class is not None:
    #         self.current_enum_changed.emit(self.get_value())

    allowNone = core.Property(  # noqa: N815
        bool,
        is_none_allowed,
        set_allow_none,
        doc="Whether None is allowed as a value",
    )
    enumValue = core.Property(  # noqa: N815
        enum.Enum,
        get_value,
        set_value,
        user=True,
        doc="Currently chosen value",
    )
    # enumClass = core.Property(type(enum.Enum), get_enum_class, set_enum_class)


if __name__ == "__main__":
    from prettyqt import constants

    app = widgets.app()
    cb = EnumComboBox(allow_none=False)
    cb.set_value(constants.ItemDataRole.EditRole)
    cb.show()
    cb.value_changed.connect(print)
    app.exec()
