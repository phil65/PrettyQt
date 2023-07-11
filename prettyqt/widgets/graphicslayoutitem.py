from __future__ import annotations

import functools

from prettyqt import widgets
from prettyqt.utils import get_repr


class GraphicsLayoutItemMixin:
    def __repr__(self):
        return get_repr(self)

    def __bool__(self):
        return not self.isEmpty()

    @functools.singledispatchmethod
    def set_size_policy(
        self,
        horizontal: widgets.sizepolicy.SizePolicyStr,
        vertical: widgets.sizepolicy.SizePolicyStr,
        control_type: widgets.sizepolicy.ControlTypeStr = "default",
    ):
        """Set the size policy.

        Args:
            horizontal: horizontal size policy
            vertical: vertical size policy
            control_type: control type associated with the widget
        """
        h_policy = widgets.sizepolicy.SIZE_POLICY[horizontal]
        v_policy = widgets.sizepolicy.SIZE_POLICY[vertical]
        c = widgets.sizepolicy.CONTROL_TYPE[control_type]
        self.setSizePolicy(h_policy, v_policy, c)

    @set_size_policy.register
    def _(self, policy: widgets.QSizePolicy):
        self.setSizePolicy(policy)

    def get_size_policy(self) -> widgets.SizePolicy:
        qpol = self.sizePolicy()
        return widgets.SizePolicy.clone(qpol)


class GraphicsLayoutItem(GraphicsLayoutItemMixin, widgets.QGraphicsLayoutItem):
    """Can be inherited to allow your custom items to be managed by layouts."""


if __name__ == "__main__":
    item = GraphicsLayoutItem()
    item.set_size_policy(widgets.SizePolicy())
