# -*- coding: utf-8 -*-

from qtpy import QtWidgets

from prettyqt import widgets


QtWidgets.QSpacerItem.__bases__ = (widgets.LayoutItem,)


class SpacerItem(QtWidgets.QSpacerItem):
    def __init__(self, w, h, h_policy, v_policy):
        if h_policy in widgets.sizepolicy.SIZE_POLICIES:
            h_policy = widgets.sizepolicy.SIZE_POLICIES[h_policy]
        if v_policy in widgets.sizepolicy.SIZE_POLICIES:
            v_policy = widgets.sizepolicy.SIZE_POLICIES[v_policy]
        super().__init__(w, h, h_policy, v_policy)

    def change_size(self, w, h, h_policy="minimum", v_policy="minimum"):
        if h_policy in widgets.sizepolicy.SIZE_POLICIES:
            h_policy = widgets.sizepolicy.SIZE_POLICIES[h_policy]
        if v_policy in widgets.sizepolicy.SIZE_POLICIES:
            v_policy = widgets.sizepolicy.SIZE_POLICIES[v_policy]
        self.changeSize(w, h, h_policy, v_policy)
