from typing import Any, Iterable, Literal, Mapping, Tuple, Union

from qtpy import QtCore, QtWidgets

from prettyqt import core, gui, widgets
from prettyqt.utils import InvalidParamError, bidict


INSERT_POLICY = bidict(
    no_insert=QtWidgets.QComboBox.NoInsert,
    top=QtWidgets.QComboBox.InsertAtTop,
    current=QtWidgets.QComboBox.InsertAtCurrent,
    bottom=QtWidgets.QComboBox.InsertAtBottom,
    after_current=QtWidgets.QComboBox.InsertAfterCurrent,
    before_current=QtWidgets.QComboBox.InsertBeforeCurrent,
    alphabetically=QtWidgets.QComboBox.InsertAlphabetically,
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
    content=QtWidgets.QComboBox.AdjustToContents,
    first_show=QtWidgets.QComboBox.AdjustToContentsOnFirstShow,
    min_length=QtWidgets.QComboBox.AdjustToMinimumContentsLength,
    min_length_with_icon=QtWidgets.QComboBox.AdjustToMinimumContentsLengthWithIcon,
)

SizeAdjustPolicyStr = Literal[
    "content", "first_show", "min_length", "min_length_with_icon"
]


class NoData:
    pass


QtWidgets.QComboBox.__bases__ = (widgets.Widget,)


class ComboBox(QtWidgets.QComboBox):

    value_changed = core.Signal(object)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.currentIndexChanged.connect(self.index_changed)

    def serialize_fields(self):
        items = [
            (self.itemText(i), self.itemData(i), self.item_icon(i))
            for i in range(self.count())
        ]
        dct = dict(
            index=self.currentIndex(),
            editable=self.isEditable(),
            max_count=self.maxCount(),
            has_frame=self.hasFrame(),
            icon_size=self.iconSize(),
            insert_policy=self.insertPolicy(),
            model_column=self.modelColumn(),
            max_visible_items=self.maxVisibleItems(),
            size_adjust_policy=self.get_size_adjust_policy(),
            duplicates_enabled=self.duplicatesEnabled(),
            min_contents_length=self.minimumContentsLength(),
            items=items,
        )
        if core.VersionNumber.get_qt_version() >= (5, 15, 0):
            dct["placeholder_text"] = self.placeholderText()
        return dct

    def __setstate__(self, state):
        for label, data, icon in state["items"]:
            self.add(label, data, icon=icon)
        self.set_id(state.get("object_name", ""))
        self.setCurrentIndex(state["index"])
        self.setEnabled(state.get("enabled", True))
        self.setToolTip(state.get("tool_tip", ""))
        self.setStatusTip(state.get("status_tip", ""))
        self.setEditable(state["editable"])
        self.setMaxCount(state["max_count"])
        self.setMaxVisibleItems(state["max_visible_items"])
        self.setMinimumContentsLength(state["min_contents_length"])
        self.setDuplicatesEnabled(state["duplicates_enabled"])
        self.setFrame(state["has_frame"])

    def __reduce__(self):
        return type(self), (), self.__getstate__()

    def __len__(self) -> int:
        return self.count()

    def index_changed(self, index: int):
        data = self.itemData(index)
        self.value_changed.emit(data)

    def add_items(self, items: Union[Iterable, Mapping], default=NoData):
        if isinstance(items, Mapping):
            for k, v in items.items():
                self.addItem(v, userData=k)
        else:
            for i in items:
                if isinstance(i, (tuple, list)):
                    self.add(*i)
                else:
                    self.addItem(i, i)
        if default is not NoData:
            self.set_value(default)

    def add(self, label: str, data=NoData, icon: gui.icon.IconType = None):
        if data is NoData:
            data = label
        if icon is not None:
            icon = gui.icon.get_icon(icon)
            self.addItem(gui.Icon(icon), label, userData=data)
        else:
            self.addItem(label, userData=data)

    def item_icon(self, index: int) -> gui.Icon:
        return gui.Icon(self.itemIcon(index))

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
        policy = SIZE_ADJUST_POLICY[policy]
        self.setSizeAdjustPolicy(policy)

    def get_size_adjust_policy(self) -> SizeAdjustPolicyStr:
        """Return size adjust policy.

        Returns:
            size adjust policy
        """
        return SIZE_ADJUST_POLICY.inverse[self.sizeAdjustPolicy()]

    def set_icon_size(self, size: Union[int, Tuple[int, int], QtCore.QSize]):
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


if __name__ == "__main__":
    app = widgets.app()
    widget = ComboBox()
    widget.value_changed.connect(print)
    w = ComboBox()
    widget.add("test", data="aa", icon="mdi.timer")
    widget.add("test2", data="aa2", icon="mdi.timer")
    widget.show()
    app.main_loop()
