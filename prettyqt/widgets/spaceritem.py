from __future__ import annotations

from prettyqt import widgets


class SpacerItem(widgets.LayoutItemMixin, widgets.QSpacerItem):
    """Blank space in a layout."""

    def __init__(
        self,
        w: int,
        h: int,
        h_policy: widgets.QSizePolicy.Policy
        | widgets.sizepolicy.SizePolicyStr = "minimum",
        v_policy: widgets.QSizePolicy.Policy
        | widgets.sizepolicy.SizePolicyStr = "minimum",
    ):
        if isinstance(h_policy, widgets.QSizePolicy.Policy):
            h_pol = h_policy
        else:
            h_pol = widgets.sizepolicy.SIZE_POLICY[h_policy]
        if isinstance(v_policy, widgets.QSizePolicy.Policy):
            v_pol = v_policy
        else:
            v_pol = widgets.sizepolicy.SIZE_POLICY[v_policy]
        super().__init__(w, h, h_pol, v_pol)

    def change_size(
        self,
        w: int,
        h: int,
        h_policy: widgets.sizepolicy.SizePolicyStr = "minimum",
        v_policy: widgets.sizepolicy.SizePolicyStr = "minimum",
    ):
        h_pol = widgets.sizepolicy.SIZE_POLICY[h_policy]
        v_pol = widgets.sizepolicy.SIZE_POLICY[v_policy]
        self.changeSize(w, h, h_pol, v_pol)

    def get_size_policy(self) -> widgets.SizePolicy:
        return widgets.SizePolicy.clone(self.sizePolicy())
