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


class AbstractScrollAreaMixin(widgets.FrameMixin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setHorizontalScrollBar(widgets.ScrollBar(parent=self))
        self.setVerticalScrollBar(widgets.ScrollBar(parent=self))

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

    def scroll_by_pixels(self, x: int = 0, y: int = 0):
        new_x = self.h_scrollbar.value() + x
        x_val = max(min(new_x, self.h_scrollbar.maximum()), self.h_scrollbar.minimum())
        new_y = self.h_scrollbar.value() + y
        y_val = max(min(new_y, self.v_scrollbar.maximum()), self.v_scrollbar.minimum())
        self.h_scrollbar.setValue(x_val)
        self.v_scrollbar.setValue(y_val)

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

    def set_scrollbar_smooth(self, value: bool = True):
        if value:
            self.h_scrollbar = widgets.SmoothScrollBar("horizontal", parent=self)
            self.v_scrollbar = widgets.SmoothScrollBar("vertical", parent=self)
        else:
            self.h_scrollbar = widgets.ScrollBar(parent=self)
            self.v_scrollbar = widgets.ScrollBar(parent=self)

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

    def set_viewport_margins(self, margins: int):
        self.setViewportMargins(margins, margins, margins, margins)


class AbstractScrollArea(AbstractScrollAreaMixin, QtWidgets.QAbstractScrollArea):
    pass


if __name__ == "__main__":
    app = widgets.app()
    widget = widgets.PlainTextEdit()
    widget.show()
    app.main_loop()
