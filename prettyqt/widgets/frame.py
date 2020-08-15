# -*- coding: utf-8 -*-

from qtpy import QtWidgets

from prettyqt import widgets
from prettyqt.utils import bidict, InvalidParamError


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
    def set_frame_shadow(self, style: str):
        """Set frame shadow.

        Allowed values are "plain", "raised", "sunken"

        Args:
            style: frame style to use

        Raises:
            InvalidParamError: style does not exist
        """
        if style not in SHADOWS:
            raise InvalidParamError(style, SHADOWS)
        self.setFrameShadow(SHADOWS[style])

    def get_frame_shadow(self) -> str:
        """Return current frame shadow.

        Possible values: "plain", "raised", "sunken"

        Returns:
            frame style
        """
        return SHADOWS.inv[self.frameShadow()]

    def set_frame_shape(self, shape: str):
        """Set frame shape.

        Allowed values are "plain", "raised", "sunken"

        Args:
            shape: frame shape to use

        Raises:
            InvalidParamError: shape does not exist
        """
        if shape not in SHAPES:
            raise InvalidParamError(shape, SHAPES)
        self.setFrameShape(SHAPES[shape])

    def get_frame_shape(self) -> str:
        """Return current frame shape.

        Possible values: "plain", "raised", "sunken"

        Returns:
            frame shape
        """
        return SHAPES.inv[self.frameShape()]
