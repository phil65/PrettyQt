from __future__ import annotations

from collections.abc import Iterable, Mapping
from typing import Any, Literal

from prettyqt import core, gui, iconprovider, widgets
from prettyqt.qt import QtWidgets
from prettyqt.utils import InvalidParamError, bidict, datatypes


mod = QtWidgets.QComboBox

INSERT_POLICY = bidict(
    no_insert=mod.InsertPolicy.NoInsert,
    top=mod.InsertPolicy.InsertAtTop,
    current=mod.InsertPolicy.InsertAtCurrent,
    bottom=mod.InsertPolicy.InsertAtBottom,
    after_current=mod.InsertPolicy.InsertAfterCurrent,
    before_current=mod.InsertPolicy.InsertBeforeCurrent,
    alphabetically=mod.InsertPolicy.InsertAlphabetically,
)

InsertPolicyStr = Literal[
    "no_insert",
    "top",
    "current",
    "bottom",
    "after_current",
    "before_current",
    "alphabetically",
]

SIZE_ADJUST_POLICY = bidict(
    content=mod.SizeAdjustPolicy.AdjustToContents,
    first_show=mod.SizeAdjustPolicy.AdjustToContentsOnFirstShow,
    # min_length=mod.SizeAdjustPolicy.AdjustToMinimumContentsLength,
    min_length_with_icon=mod.SizeAdjustPolicy.AdjustToMinimumContentsLengthWithIcon,
)

SizeAdjustPolicyStr = Literal[
    "content",
    "first_show",
    # "min_length",
    "min_length_with_icon",
]


class ComboBoxMixin(widgets.WidgetMixin):
    value_changed = core.Signal(object)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.currentIndexChanged.connect(self._index_changed)

    def _get_map(self):
        maps = super()._get_map()
        maps |= {
            "insertPolicy": INSERT_POLICY,
            "sizeAdjustPolicy": SIZE_ADJUST_POLICY,
        }
        return maps

    # def __reduce__(self):
    #     return type(self), (), self.__getstate__()

    def __len__(self) -> int:
        return self.count()

    def _index_changed(self, index: int):
        # data = self.itemData(index)
        data = self.get_value()
        self.value_changed.emit(data)

    def add_items(
        self, items: Iterable[str | tuple | list] | Mapping[Any, str], default=...
    ):
        if isinstance(items, Mapping):
            for k, v in items.items():
                self.addItem(v, userData=k)
        else:
            for i in items:
                if isinstance(i, tuple | list):
                    self.add(*i)
                else:
                    self.addItem(i, i)
        if default is not ...:
            self.set_value(default)

    def add(self, label: str, data=..., icon: datatypes.IconType = None):
        if data is ...:
            data = label
        if icon is not None:
            icon = iconprovider.get_icon(icon)
            self.addItem(gui.Icon(icon), label, userData=data)
        else:
            self.addItem(label, userData=data)

    def get_item_icon(self, index: int) -> gui.Icon | None:
        icon = self.itemIcon(index)
        return None if icon.isNull() else gui.Icon(icon)

    def set_editable(self, editable: bool):
        self.setEditable(editable)
        if self.completer() is None and editable:
            self.setCompleter(widgets.Completer(self))

    def set_insert_policy(self, policy: InsertPolicyStr):
        """Set insert policy.

        Args:
            policy: insert policy to use

        Raises:
            InvalidParamError: invalid insert policy
        """
        if policy not in INSERT_POLICY:
            raise InvalidParamError(policy, INSERT_POLICY)
        self.setInsertPolicy(INSERT_POLICY[policy])

    def get_insert_policy(self) -> InsertPolicyStr:
        """Return insert policy.

        Returns:
            insert policy
        """
        return INSERT_POLICY.inverse[self.insertPolicy()]

    def set_size_adjust_policy(self, policy: SizeAdjustPolicyStr):
        """Set size adjust policy.

        Args:
            policy: size adjust policy to use

        Raises:
            InvalidParamError: invalid size adjust policy
        """
        if policy not in SIZE_ADJUST_POLICY:
            raise InvalidParamError(policy, SIZE_ADJUST_POLICY)
        self.setSizeAdjustPolicy(SIZE_ADJUST_POLICY[policy])

    def get_size_adjust_policy(self) -> SizeAdjustPolicyStr:
        """Return size adjust policy.

        Returns:
            size adjust policy
        """
        return SIZE_ADJUST_POLICY.inverse[self.sizeAdjustPolicy()]

    def set_icon_size(self, size: int | datatypes.SizeType):
        """Set size of the icons."""
        if isinstance(size, int):
            size = core.Size(size, size)
        elif isinstance(size, tuple):
            size = core.Size(*size)
        self.setIconSize(size)

    def get_icon_size(self) -> core.Size:
        return core.Size(self.iconSize())

    def set_min_char_length(self, chars: int):
        self.setMinimumContentsLength(chars)

    def get_value(self) -> Any:
        # if all(self.itemData(i) is None for i in range(self.count())):
        #     return self.currentText()
        # else:
        #     return self.currentData()
        return self.currentData()

    def set_value(self, value: Any):
        self.set_data(value)

    def set_text(self, text: str):
        self.setCurrentText(text)

    def set_data(self, data: Any):
        idx = self.findData(data)
        if idx == -1:
            raise ValueError("invalid data")
        self.setCurrentIndex(idx)

    def text(self) -> str:
        return self.currentText()

    def hide_completer(self):
        """Hides the completion widget."""
        completer = widgets.Completer(self)
        self.setCompleter(completer)


class ComboBox(ComboBoxMixin, QtWidgets.QComboBox):
    pass


if __name__ == "__main__":
    app = widgets.app()
    widget = ComboBox()
    w = ComboBox()
    widget.add("test", data="aa", icon="mdi.timer")
    widget.add("test2", data="aa2", icon="mdi.timer")
    widget.show()
    app.main_loop()
