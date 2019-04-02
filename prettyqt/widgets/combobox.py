# -*- coding: utf-8 -*-
"""
@author: Philipp Temminghoff
"""

from qtpy import QtWidgets, QtCore


INSERT_POLICIES = dict(no_insert=QtWidgets.QComboBox.NoInsert,
                       top=QtWidgets.QComboBox.InsertAtTop,
                       current=QtWidgets.QComboBox.InsertAtCurrent,
                       bottom=QtWidgets.QComboBox.InsertAtBottom,
                       after_current=QtWidgets.QComboBox.InsertAfterCurrent,
                       before_current=QtWidgets.QComboBox.InsertBeforeCurrent,
                       alphabetically=QtWidgets.QComboBox.InsertAlphabetically)

SIZE_POLICIES = dict(content=QtWidgets.QComboBox.AdjustToContents,
                     first_show=QtWidgets.QComboBox.AdjustToContentsOnFirstShow,
                     min_length=QtWidgets.QComboBox.AdjustToMinimumContentsLength,
                     min_length_with_icon=QtWidgets.QComboBox.AdjustToMinimumContentsLengthWithIcon)


class ComboBox(QtWidgets.QComboBox):

    def set_enabled(self):
        self.setEnabled(True)

    def set_disabled(self):
        self.setEnabled(False)

    def add_item(self, label, data=None, icon=None):
        if icon is not None:
            self.addItem(icon, label, userData=data)
        else:
            self.addItem(label, userData=data)

    def set_insert_policy(self, policy):
        if policy not in INSERT_POLICIES:
            raise ValueError("Policy not available")
        policy = INSERT_POLICIES.get(policy)
        self.setInsertPolicy(policy)

    def set_size_policy(self, policy):
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

    def set_min_char_length(self, chars):
        self.setMinimumContentsLength(chars)


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    widget = ComboBox()
    widget.add_item("test", data="aa")
    widget.show()
    app.exec_()
