# -*- coding: utf-8 -*-
"""
"""

from qtpy import QtWidgets

from prettyqt import widgets


QtWidgets.QSpacerItem.__bases__ = (widgets.LayoutItem,)

SIZE_POLICIES = widgets.sizepolicy.SIZE_POLICIES


class SpacerItem(QtWidgets.QSpacerItem):
    def __init__(self, w, h, h_policy, v_policy):
        if h_policy in SIZE_POLICIES:
            h_policy = SIZE_POLICIES[h_policy]
        if v_policy in SIZE_POLICIES:
            v_policy = SIZE_POLICIES[v_policy]
        super().__init__(w, h, h_policy, v_policy)

    def change_size(self, w, h, h_policy="minimum", v_policy="minimum"):
        if h_policy in SIZE_POLICIES:
            h_policy = SIZE_POLICIES[h_policy]
        if v_policy in SIZE_POLICIES:
            v_policy = SIZE_POLICIES[v_policy]
        self.changeSize(w, h, h_policy, v_policy)
