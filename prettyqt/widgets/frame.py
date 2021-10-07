from __future__ import annotations

from typing import Literal

from prettyqt import widgets
from prettyqt.qt import QtWidgets
from prettyqt.utils import InvalidParamError, bidict


SHADOW = bidict(
    plain=QtWidgets.QFrame.Shadow.Plain,
    raised=QtWidgets.QFrame.Shadow.Raised,
    sunken=QtWidgets.QFrame.Shadow.Sunken,
)

ShadowStr = Literal["plain", "raised", "sunken"]

FRAME_SHAPE = bidict(
    no_frame=QtWidgets.QFrame.Shape.NoFrame,
    box=QtWidgets.QFrame.Shape.Box,
    panel=QtWidgets.QFrame.Shape.Panel,
    styled_panel=QtWidgets.QFrame.Shape.StyledPanel,
    h_line=QtWidgets.QFrame.Shape.HLine,
    v_line=QtWidgets.QFrame.Shape.VLine,
    win_panel=QtWidgets.QFrame.Shape.WinPanel,
)

FrameShapeStr = Literal[
    "no_frame", "box", "panel", "styled_panel", "h_line", "v_line", "win_panel"
]


QtWidgets.QFrame.__bases__ = (widgets.Widget,)


class Frame(QtWidgets.QFrame):
    def serialize_fields(self):
        return dict(
            frame_shadow=self.get_frame_shadow(),
            frame_shape=self.get_frame_shape(),
            frame_rect=self.frameRect(),
        )

    def __setstate__(self, state):
        super().__setstate__(state)
        self.set_frame_shadow(state["frame_shadow"])
        self.set_frame_shape(state["frame_shape"])
        self.setFrameRect(state["frame_rect"])

    def set_frame_shadow(self, style: ShadowStr):
        """Set frame shadow.

        Args:
            style: frame style to use

        Raises:
            InvalidParamError: style does not exist
        """
        if style is None:
            return
        if style not in SHADOW:
            raise InvalidParamError(style, SHADOW)
        self.setFrameShadow(SHADOW[style])

    def get_frame_shadow(self) -> ShadowStr | None:
        """Return current frame shadow.

        Returns:
            frame style
        """
        if (frame_shadow := self.frameShadow()) == 0:
            return None
        return SHADOW.inverse[frame_shadow]

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
