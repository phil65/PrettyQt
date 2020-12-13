from typing import Union

from qtpy import QtWidgets

from prettyqt import widgets


QtWidgets.QSpacerItem.__bases__ = (widgets.LayoutItem,)


class SpacerItem(QtWidgets.QSpacerItem):
    def __init__(
        self,
        w: int,
        h: int,
        h_policy: Union[int, widgets.sizepolicy.SizePolicyStr],
        v_policy: Union[int, widgets.sizepolicy.SizePolicyStr],
    ):
        if h_policy in widgets.sizepolicy.SIZE_POLICY:
            h_policy = widgets.sizepolicy.SIZE_POLICY[h_policy]
        if v_policy in widgets.sizepolicy.SIZE_POLICY:
            v_policy = widgets.sizepolicy.SIZE_POLICY[v_policy]
        super().__init__(w, h, h_policy, v_policy)

    def change_size(
        self,
        w: int,
        h: int,
        h_policy: widgets.sizepolicy.SizePolicyStr = "minimum",
        v_policy: widgets.sizepolicy.SizePolicyStr = "minimum",
    ):
        if h_policy in widgets.sizepolicy.SIZE_POLICY:
            h_policy = widgets.sizepolicy.SIZE_POLICY[h_policy]
        if v_policy in widgets.sizepolicy.SIZE_POLICY:
            v_policy = widgets.sizepolicy.SIZE_POLICY[v_policy]
        self.changeSize(w, h, h_policy, v_policy)
