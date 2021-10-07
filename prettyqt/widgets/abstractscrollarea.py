from __future__ import annotations

from typing import Literal

from prettyqt import constants, widgets
from prettyqt.qt import QtWidgets
from prettyqt.utils import InvalidParamError, bidict


area = QtWidgets.QAbstractScrollArea

SIZE_POLICY = bidict(
    content=area.SizeAdjustPolicy.AdjustToContents,
    first_show=area.SizeAdjustPolicy.AdjustToContentsOnFirstShow,
    ignored=area.SizeAdjustPolicy.AdjustIgnored,
)

SizePolicyStr = Literal["content", "first_show", "ignored"]


QtWidgets.QAbstractScrollArea.__bases__ = (widgets.Frame,)


class AbstractScrollArea(QtWidgets.QAbstractScrollArea):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setHorizontalScrollBar(widgets.ScrollBar(parent=self))
        self.setVerticalScrollBar(widgets.ScrollBar(parent=self))

    def serialize_fields(self):
        return dict(
            size_adjust_policy=self.get_size_adjust_policy(),
            horizontal_scrollbar_policy=self.get_horizontal_scrollbar_policy(),
            vertical_scrollbar_policy=self.get_vertical_scrollbar_policy(),
        )

    def __setstate__(self, state):
        super().__setstate__(state)
        self.set_size_adjust_policy(state["size_adjust_policy"])
        self.set_horizontal_scrollbar_policy(state["horizontal_scrollbar_policy"])
        self.set_vertical_scrollbar_policy(state["vertical_scrollbar_policy"])

    @property
    def h_scrollbar(self):
        return self.horizontalScrollBar()

    @h_scrollbar.setter
    def h_scrollbar(self, scrollbar):
        self.setHorizontalScrollBar(scrollbar)

    @property
    def v_scrollbar(self):
        return self.verticalScrollBar()

    @v_scrollbar.setter
    def v_scrollbar(self, scrollbar):
        self.setVerticalScrollBar(scrollbar)

    def set_size_adjust_policy(self, policy: SizePolicyStr):
        """Set size adjust policy.

        Args:
            policy: size adjust policy to use

        Raises:
            InvalidParamError: invalid size adjust policy
        """
        if policy not in SIZE_POLICY:
            raise InvalidParamError(policy, SIZE_POLICY)
        self.setSizeAdjustPolicy(SIZE_POLICY[policy])

    def get_size_adjust_policy(self) -> SizePolicyStr:
        """Return size adjust policy.

        Returns:
            size adjust policy
        """
        return SIZE_POLICY.inverse[self.sizeAdjustPolicy()]

    def set_scrollbar_policy(self, mode: constants.ScrollBarPolicyStr):
        """Set the policy for both scrollbars.

        Args:
            mode: visibilty to set

        Raises:
            InvalidParamError: invalid scrollbar policy
        """
        if mode not in constants.SCROLLBAR_POLICY:
            raise InvalidParamError(mode, constants.SCROLLBAR_POLICY)
        self.setHorizontalScrollBarPolicy(constants.SCROLLBAR_POLICY[mode])
        self.setVerticalScrollBarPolicy(constants.SCROLLBAR_POLICY[mode])

    def set_horizontal_scrollbar_policy(self, mode: constants.ScrollBarPolicyStr):
        """Set the horizontal scrollbar visibility.

        Args:
            mode: visibilty to set

        Raises:
            InvalidParamError: invalid scrollbar policy
        """
        if mode not in constants.SCROLLBAR_POLICY:
            raise InvalidParamError(mode, constants.SCROLLBAR_POLICY)
        self.setHorizontalScrollBarPolicy(constants.SCROLLBAR_POLICY[mode])

    def get_horizontal_scrollbar_policy(self):
        return constants.SCROLLBAR_POLICY.inverse[self.horizontalScrollBarPolicy()]

    def set_vertical_scrollbar_policy(self, mode: constants.ScrollBarPolicyStr):
        """Set the vertical scrollbar visibility.

        Args:
            mode: visibilty to set

        Raises:
            InvalidParamError: invalid scrollbar policy
        """
        if mode not in constants.SCROLLBAR_POLICY:
            raise InvalidParamError(mode, constants.SCROLLBAR_POLICY)
        self.setVerticalScrollBarPolicy(constants.SCROLLBAR_POLICY[mode])

    def get_vertical_scrollbar_policy(self):
        return constants.SCROLLBAR_POLICY.inverse[self.verticalScrollBarPolicy()]

    def set_scrollbar_width(self, width: int):
        """Set the width for both scrollbars.

        Args:
            width: width in pixels
        """
        self.set_horizontal_scrollbar_width(width)
        self.set_vertical_scrollbar_width(width)

    def set_horizontal_scrollbar_width(self, width: int):
        """Set the horizontal scrollbar width.

        Args:
            width: width in pixels
        """
        with self.h_scrollbar.edit_stylesheet() as ss:
            ss.QScrollBar.horizontal.height.setValue(f"{width}px")

    def set_vertical_scrollbar_width(self, width: int):
        """Set the vertical scrollbar width.

        Args:
            width: width in pixels
        """
        with self.v_scrollbar.edit_stylesheet() as ss:
            ss.QScrollBar.horizontal.height.setValue(f"{width}px")

    def scroll_to_top(self):
        """Scroll to the top of the scroll area."""
        self.verticalScrollBar().scroll_to_min()

    def scroll_to_bottom(self):
        """Scroll to the bottom of the scroll area."""
        self.verticalScrollBar().scroll_to_max()


if __name__ == "__main__":
    app = widgets.app()
    widget = AbstractScrollArea()
    widget.show()
    app.main_loop()
