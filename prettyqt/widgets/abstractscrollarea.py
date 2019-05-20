# -*- coding: utf-8 -*-
"""
@author: Philipp Temminghoff
"""

from bidict import bidict

from qtpy import QtWidgets, QtCore

from prettyqt import widgets

area = QtWidgets.QAbstractScrollArea

SIZE_POLICIES = bidict(dict(content=area.AdjustToContents,
                            first_show=area.AdjustToContentsOnFirstShow,
                            ignored=area.AdjustIgnored))


SCROLLBAR_POLICY = bidict(dict(always_on=QtCore.Qt.ScrollBarAlwaysOn,
                               always_off=QtCore.Qt.ScrollBarAlwaysOff,
                               as_needed=QtCore.Qt.ScrollBarAsNeeded))


class AbstractScrollArea(QtWidgets.QAbstractScrollArea):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.h_scrollbar = widgets.ScrollBar()
        self.v_scrollbar = widgets.ScrollBar()

    @property
    def h_scrollbar(self):
        return self.horizontalScrollbar()

    @h_scrollbar.setter
    def h_scrollbar(self, scrollbar):
        self.setHorizontalScrollBar(scrollbar)

    @property
    def v_scrollbar(self):
        return self.verticalScrollBar()

    @v_scrollbar.setter
    def v_scrollbar(self, scrollbar):
        self.setVerticalScrollBar(scrollbar)

    def set_size_adjust_policy(self, policy: str):
        """set size adjust policy

        Valid values are "content", "first_show", "ignored"

        Args:
            policy: size adjust policy to use

        Raises:
            ValueError: invalid size adjust policy
        """
        if policy not in SIZE_POLICIES:
            raise ValueError("Policy not available")
        policy = SIZE_POLICIES.get(policy)
        self.setSizeAdjustPolicy(policy)

    def get_size_adjust_policy(self) -> str:
        """returns size adjust policy

        possible values are "content", "first_show", "ignored"

        Returns:
            size adjust policy
        """
        return SIZE_POLICIES.inv[self.sizeAdjustPolicy()]

    def set_horizontal_scrollbar_policy(self, mode: str):
        """sets the horizontal scrollbar visibility

        possible values are "always_on", "always_off", "as_needed"

        Args:
            mode: visibilty to set

        Raises:
            ValueError: invalid scrollbar policy
        """
        if mode not in SCROLLBAR_POLICY:
            raise ValueError("Invalid scrollbar policy")
        self.setHorizontalScrollBarPolicy(SCROLLBAR_POLICY[mode])

    def set_vertical_scrollbar_policy(self, mode: str):
        """sets the vertical scrollbar visibility

        possible values are "always_on", "always_off", "as_needed"

        Args:
            mode: visibilty to set

        Raises:
            ValueError: invalid scrollbar policy
        """
        if mode not in SCROLLBAR_POLICY:
            raise ValueError("Invalid scrollbar policy")
        self.setVerticalScrollBarPolicy(SCROLLBAR_POLICY[mode])

    def set_horizontal_scrollbar_width(self, width: int):
        """sets the horizontal scrollbar width

        Args:
            width: width in pixels
        """
        stylesheet = f"QScrollBar:horizontal {{height: {width}px;}}"
        self.horizontalScrollBar().setStyleSheet(stylesheet)

    def set_vertical_scrollbar_width(self, width: int):
        """sets the vertical scrollbar width

        Args:
            width: width in pixels
        """
        stylesheet = f"QScrollBar:vertical {{height: {width}px;}}"
        self.verticalScrollBar().setStyleSheet(stylesheet)

    def scroll_to_top(self):
        """scroll to the top of the scroll area
        """
        self.verticalScrollBar().scroll_to_min()

    def scroll_to_bottom(self):
        """scroll to the bottom of the scroll area
        """
        self.verticalScrollBar().scroll_to_max()


AbstractScrollArea.__bases__[0].__bases__ = (widgets.Frame,)


if __name__ == "__main__":
    app = widgets.app()
    widget = AbstractScrollArea()
    widget.show()
    app.exec_()
