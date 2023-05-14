from __future__ import annotations

from typing import Literal

from prettyqt import widgets
from prettyqt.qt import QtCore, QtWidgets
from prettyqt.utils import InvalidParamError, bidict, datatypes


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


class FrameMixin(widgets.WidgetMixin):
    def _get_map(self):
        maps = super()._get_map()
        maps |= {"frameShape": FRAME_SHAPE, "frameShadow": SHADOW}
        return maps

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

    def set_frame_rect(self, rect: datatypes.RectType | None):
        if isinstance(rect, tuple):
            rect = QtCore.QRect(*rect)
        elif rect is None:
            rect = QtCore.QRect(0, 0, 0, 0)


class Frame(FrameMixin, QtWidgets.QFrame):
    pass


if __name__ == "__main__":
    app = widgets.app()
    widget = Frame(frame_shape="panel", object_name="fff")
    print(widget.get_properties())
    widget.show()
    app.main_loop()
