# -*- coding: utf-8 -*-
"""
"""

from qtpy import QtWidgets

from prettyqt import widgets
from prettyqt.utils import bidict


SHADOWS = bidict(
    plain=QtWidgets.QFrame.Plain,
    raised=QtWidgets.QFrame.Raised,
    sunken=QtWidgets.QFrame.Sunken,
)

SHAPES = bidict(
    no_frame=QtWidgets.QFrame.NoFrame,
    box=QtWidgets.QFrame.Box,
    panel=QtWidgets.QFrame.Panel,
    styled_panel=QtWidgets.QFrame.StyledPanel,
    h_line=QtWidgets.QFrame.HLine,
    v_line=QtWidgets.QFrame.VLine,
    win_panel=QtWidgets.QFrame.WinPanel,
)

QtWidgets.QFrame.__bases__ = (widgets.Widget,)


class Frame(QtWidgets.QFrame):
    def set_frame_style(self, style: str):
        """set frame style

        Allowed values are "plain", "raised", "sunken"

        Args:
            style: frame style to use

        Raises:
            ValueError: style does not exist
        """
        if style not in SHADOWS:
            raise ValueError("invalid frame style")
        self.setFrameStyle(SHADOWS[style])

    def get_frame_style(self) -> str:
        """returns current frame style

        Possible values: "plain", "raised", "sunken"

        Returns:
            frame style
        """
        return SHADOWS.inv[self.frameStyle()]
