from typing import Literal

from qtpy import QtWidgets

from prettyqt import widgets
from prettyqt.utils import InvalidParamError, bidict


SHADOW = bidict(
    plain=QtWidgets.QFrame.Plain,
    raised=QtWidgets.QFrame.Raised,
    sunken=QtWidgets.QFrame.Sunken,
)

ShadowStr = Literal["plain", "raised", "sunken"]

FRAME_SHAPE = bidict(
    no_frame=QtWidgets.QFrame.NoFrame,
    box=QtWidgets.QFrame.Box,
    panel=QtWidgets.QFrame.Panel,
    styled_panel=QtWidgets.QFrame.StyledPanel,
    h_line=QtWidgets.QFrame.HLine,
    v_line=QtWidgets.QFrame.VLine,
    win_panel=QtWidgets.QFrame.WinPanel,
)

FrameShapeStr = Literal[
    "no_frame", "box", "panel", "styled_panel", "h_line", "v_line", "win_panel"
]


QtWidgets.QFrame.__bases__ = (widgets.Widget,)


class Frame(QtWidgets.QFrame):
    def set_frame_shadow(self, style: ShadowStr):
        """Set frame shadow.

        Args:
            style: frame style to use

        Raises:
            InvalidParamError: style does not exist
        """
        if style not in SHADOW:
            raise InvalidParamError(style, SHADOW)
        self.setFrameShadow(SHADOW[style])

    def get_frame_shadow(self) -> ShadowStr:
        """Return current frame shadow.

        Returns:
            frame style
        """
        return SHADOW.inverse[self.frameShadow()]

    def set_frame_shape(self, shape: FrameShapeStr):
        """Set frame shape.

        Args:
            shape: frame shape to use

        Raises:
            InvalidParamError: shape does not exist
        """
        if shape not in FRAME_SHAPE:
            raise InvalidParamError(shape, FRAME_SHAPE)
        self.setFrameShape(FRAME_SHAPE[shape])

    def get_frame_shape(self) -> FrameShapeStr:
        """Return current frame shape.

        Returns:
            frame shape
        """
        return FRAME_SHAPE.inverse[self.frameShape()]
