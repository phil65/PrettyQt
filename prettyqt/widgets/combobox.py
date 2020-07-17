# -*- coding: utf-8 -*-
"""
"""

from typing import Iterable, Union, Mapping, Any

from qtpy import QtCore, QtWidgets

from prettyqt import core, gui, widgets
from prettyqt.utils import bidict


box = QtWidgets.QComboBox
INSERT_POLICIES = bidict(
    no_insert=box.NoInsert,
    top=box.InsertAtTop,
    current=box.InsertAtCurrent,
    bottom=box.InsertAtBottom,
    after_current=box.InsertAfterCurrent,
    before_current=box.InsertBeforeCurrent,
    alphabetically=box.InsertAlphabetically,
)

SIZE_POLICIES = bidict(
    content=box.AdjustToContents,
    first_show=box.AdjustToContentsOnFirstShow,
    min_length=box.AdjustToMinimumContentsLength,
    min_length_with_icon=box.AdjustToMinimumContentsLengthWithIcon,
)


class NoData(object):
    pass


QtWidgets.QComboBox.__bases__ = (widgets.Widget,)


class ComboBox(QtWidgets.QComboBox):

    value_changed = core.Signal(object)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.currentIndexChanged.connect(self.index_changed)

    def __getstate__(self):
        items = [
            (self.itemText(i), self.itemData(i), self.item_icon(i))
            for i in range(self.count())
        ]
        return dict(
            object_name=self.id,
            index=self.currentIndex(),
            enabled=self.isEnabled(),
            editable=self.isEditable(),
            tooltip=self.toolTip(),
            statustip=self.statusTip(),
            max_count=self.maxCount(),
            has_frame=self.hasFrame(),
            max_visible_items=self.maxVisibleItems(),
            duplicates_enabled=self.duplicatesEnabled(),
            min_contents_length=self.minimumContentsLength(),
            items=items,
        )

    def __setstate__(self, state):
        self.__init__()
        for label, data, icon in state["items"]:
            self.add(label, data, icon=icon)
        self.set_id(state.get("object_name", ""))
        self.setCurrentIndex(state["index"])
        self.setEnabled(state.get("enabled", True))
        self.setToolTip(state.get("tooltip", ""))
        self.setStatusTip(state.get("statustip", ""))
        self.setEditable(state["editable"])
        self.setMaxCount(state["max_count"])
        self.setMaxVisibleItems(state["max_visible_items"])
        self.setMinimumContentsLength(state["min_contents_length"])
        self.setDuplicatesEnabled(state["duplicates_enabled"])
        self.setFrame(state["has_frame"])

    def __len__(self):
        return self.count()

    def index_changed(self, index: int):
        data = self.itemData(index)
        self.value_changed.emit(data)

    def add_items(self, items: Union[Iterable, Mapping]):
        if isinstance(items, Mapping):
            for k, v in items.items():
                self.addItem(v, userData=k)
        else:
            for i in items:
                if isinstance(i, (tuple, list)):
                    self.add(*i)
                else:
                    self.addItem(i, i)

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

    def set_insert_policy(self, policy: str):
        """set insert policy

        valid values are "no_insert", "top", "current", "bottom", "after_current",
        "before_current", "alphabetically"

        Args:
            policy: insert policy to use

        Raises:
            ValueError: invalid insert policy
        """
        if policy not in INSERT_POLICIES:
            raise ValueError("Policy not available")
        policy = INSERT_POLICIES.get(policy)
        self.setInsertPolicy(policy)

    def get_insert_policy(self) -> str:
        """returns insert policy

        possible values are "no_insert", "top", "current", "bottom", "after_current",
        "before_current", "alphabetically"

        Returns:
            insert policy
        """
        return INSERT_POLICIES.inv[self.insertPolicy()]

    def set_size_adjust_policy(self, policy: str):
        """set size adjust policy

        possible values are "content", "first_show", "min_length", "min_length_with_icon"

        Args:
            policy: size adjust policy to use

        Raises:
            ValueError: invalid size adjust policy
        """
        if policy not in SIZE_POLICIES:
            raise ValueError("Policy not available")
        policy = SIZE_POLICIES.get(policy)
        self.setSizeAdjustPolicy(policy)

    def get_size_adjust_policy(self) -> str:
        """returns size adjust policy

        possible values are "content", "first_show", "min_length", "min_length_with_icon"

        Returns:
            size adjust policy
        """
        return SIZE_POLICIES.inv[self.sizeAdjustPolicy()]

    def set_icon_size(self, size: int):
        self.setIconSize(QtCore.QSize(size, size))

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
    app.exec_()
