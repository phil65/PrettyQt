# -*- coding: utf-8 -*-
"""
@author: Philipp Temminghoff
"""

from qtpy import QtCore, QtWidgets
import qtawesome as qta

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

    def __getstate__(self):
        labels = [self.itemText(i) for i in range(self.count())]
        data = [self.itemData(i) for i in range(self.count())]
        return dict(index=self.currentIndex(),
                    enabled=self.isEnabled(),
                    labels=labels,
                    data=data)

    def __setstate__(self, state):
        super().__init__()
        for label, data in zip(state["labels"], state["data"]):
            self.add_item(label, data)
        self.setCurrentIndex(state["index"])
        self.setEnabled(state["enabled"])

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
            self.addItem(icon, label, userData=data)
        else:
            self.addItem(label, userData=data)

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


if __name__ == "__main__":
    from prettyqt import widgets
    app = widgets.Application.create_default_app()
    widget = ComboBox()
    widget.add_item("test", data="aa")
    widget.show()
    app.exec_()
