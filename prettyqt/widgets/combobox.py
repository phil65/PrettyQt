# -*- coding: utf-8 -*-
"""
@author: Philipp Temminghoff
"""

import qtawesome as qta
from qtpy import QtCore, QtWidgets

from prettyqt import gui, core

box = QtWidgets.QComboBox
INSERT_POLICIES = dict(no_insert=box.NoInsert,
                       top=box.InsertAtTop,
                       current=box.InsertAtCurrent,
                       bottom=box.InsertAtBottom,
                       after_current=box.InsertAfterCurrent,
                       before_current=box.InsertBeforeCurrent,
                       alphabetically=box.InsertAlphabetically)

SIZE_POLICIES = dict(content=box.AdjustToContents,
                     first_show=box.AdjustToContentsOnFirstShow,
                     min_length=box.AdjustToMinimumContentsLength,
                     min_length_with_icon=box.AdjustToMinimumContentsLengthWithIcon)


class ComboBox(QtWidgets.QComboBox):

    value_changed = core.Signal(object)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.currentIndexChanged.connect(self.index_changed)

    def __getstate__(self):
        items = [(self.itemText(i), self.itemData(i), self.item_icon(i))
                 for i in range(self.count())]
        return dict(object_name=self.objectName(),
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
                    items=items)

    def __setstate__(self, state):
        super().__init__()
        for label, data, icon in state["items"]:
            self.add_item(label, data, icon=icon)
        self.setObjectName(state["object_name"])
        self.setCurrentIndex(state["index"])
        self.setEnabled(state["enabled"])
        self.setToolTip(state["tooltip"])
        self.setStatusTip(state["statustip"])
        self.setEditable(state["editable"])
        self.setMaxCount(state["max_count"])
        self.setMaxVisibleItems(state["max_visible_items"])
        self.setMinimumContentsLength(state["min_contents_length"])
        self.setDuplicatesEnabled(state["duplicates_enabled"])
        self.setFrame(state["has_frame"])

    def __len__(self):
        return self.count()

    def index_changed(self, index):
        data = self.itemData(index)
        self.value_changed.emit(data)

    def set_enabled(self):
        self.setEnabled(True)

    def set_disabled(self):
        self.setEnabled(False)

    def add_item(self,
                 label: str,
                 data=None,
                 icon=None):
        if icon is not None:
            if isinstance(icon, str):
                icon = qta.icon(icon)
            self.addItem(gui.Icon(icon), label, userData=data)
        else:
            self.addItem(label, userData=data)

    def item_icon(self, index):
        return gui.Icon(self.itemIcon(index))

    def set_insert_policy(self, policy: str):
        if policy not in INSERT_POLICIES:
            raise ValueError("Policy not available")
        policy = INSERT_POLICIES.get(policy)
        self.setInsertPolicy(policy)

    def set_size_policy(self, policy: str):
        """set size policy

        Args:
            policy: size policy to use

        Raises:
            ValueError: invalid size policy
        """
        if policy not in SIZE_POLICIES:
            raise ValueError("Policy not available")
        policy = SIZE_POLICIES.get(policy)
        self.setSizeAdjustPolicy(policy)

    def set_icon_size(self, size: int):
        self.setIconSize(QtCore.QSize(size, size))

    def set_min_char_length(self, chars: int):
        self.setMinimumContentsLength(chars)

    def get_value(self):
        return self.currentData()


if __name__ == "__main__":
    from prettyqt import widgets
    app = widgets.Application.create_default_app()
    widget = ComboBox()
    widget.value_changed.connect(print)
    w = ComboBox()
    widget.add_item("test", data="aa", icon="mdi.timer")
    widget.add_item("test2", data="aa2", icon="mdi.timer")
    widget.show()
    app.exec_()
