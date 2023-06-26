from __future__ import annotations

from typing import Literal

from prettyqt import widgets
from prettyqt.qt import QtWidgets
from prettyqt.utils import bidict, datatypes


ShadowStr = Literal["plain", "raised", "sunken"]

SHADOW: bidict[ShadowStr, QtWidgets.QFrame.Shadow] = bidict(
    plain=QtWidgets.QFrame.Shadow.Plain,
    raised=QtWidgets.QFrame.Shadow.Raised,
    sunken=QtWidgets.QFrame.Shadow.Sunken,
)

FrameShapeStr = Literal[
    "no_frame", "box", "panel", "styled_panel", "h_line", "v_line", "win_panel"
]

FRAME_SHAPE: bidict[FrameShapeStr, QtWidgets.QFrame.Shape] = bidict(
    no_frame=QtWidgets.QFrame.Shape.NoFrame,
    box=QtWidgets.QFrame.Shape.Box,
    panel=QtWidgets.QFrame.Shape.Panel,
    styled_panel=QtWidgets.QFrame.Shape.StyledPanel,
    h_line=QtWidgets.QFrame.Shape.HLine,
    v_line=QtWidgets.QFrame.Shape.VLine,
    win_panel=QtWidgets.QFrame.Shape.WinPanel,
)


class FrameMixin(widgets.WidgetMixin):
    def _get_map(self):
        maps = super()._get_map()
        maps |= {"frameShape": FRAME_SHAPE, "frameShadow": SHADOW}
        return maps

    def set_frame_shadow(self, style: ShadowStr | QtWidgets.QFrame.Shadow):
        """Set frame shadow.

        Args:
            style: frame style to use
        """
        self.setFrameShadow(SHADOW.get_enum_value(style))

    def get_frame_shadow(self) -> ShadowStr | None:
        """Return current frame shadow.

        Returns:
            frame style
        """
        if (frame_shadow := self.frameShadow()) == 0:
            return None
        return SHADOW.inverse[frame_shadow]

    def set_frame_shape(self, shape: FrameShapeStr | QtWidgets.QFrame.Shape):
        """Set frame shape.

        Args:
            shape: frame shape to use
        """
        self.setFrameShape(FRAME_SHAPE.get_enum_value(shape))

    def get_frame_shape(self) -> FrameShapeStr:
        """Return current frame shape.

        Returns:
            frame shape
        """
        return FRAME_SHAPE.inverse[self.frameShape()]

    def set_frame_rect(self, rect: datatypes.RectType):
        self.setFrameRect(datatypes.to_rect(rect))


class Frame(FrameMixin, QtWidgets.QFrame):
    pass


if __name__ == "__main__":
    app = widgets.app()
    widget = Frame(frame_shape="panel", object_name="fff")
    widget.show()
    app.exec()
