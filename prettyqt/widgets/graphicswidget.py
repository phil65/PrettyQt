from __future__ import annotations

from typing import Literal

from prettyqt import constants, gui, widgets
from prettyqt.qt import QtCore, QtWidgets
from prettyqt.utils import InvalidParamError, datatypes


LayoutStr = Literal["grid", "horizontal", "vertical", "anchor"]


class GraphicsWidgetMixin(widgets.GraphicsObjectMixin, widgets.GraphicsLayoutItemMixin):
    def serialize_fields(self):
        return dict(
            autofill_background=self.autoFillBackground(),
            font=self.get_font(),
            window_title=self.windowTitle(),
            preferred_size=self.preferredSize(),
            maximum_size=self.maximumSize(),
            palette=self.get_palette(),
            focus_policy=self.get_focus_policy(),
        )

    def set_layout(self, layout: LayoutStr | QtWidgets.QGraphicsLayout | None):
        match layout:
            case None:
                return
            case QtWidgets.QGraphicsLayout():
                self.box = layout
            case "grid":
                self.box = widgets.GraphicsGridLayout()
            case "anchor":
                self.box = widgets.GraphicsAnchorLayout()
            case "horizontal" | "vertical":
                self.box = widgets.GraphicsLinearLayout(layout)
            case _:
                raise ValueError("Invalid Layout")
        self.setLayout(self.box)

    def set_focus_policy(self, policy: constants.FocusPolicyStr) -> None:
        """Set the way the widget accepts keyboard focus.

        Args:
            policy: Focus policy

        Raises:
            InvalidParamError: Description
        """
        if policy not in constants.FOCUS_POLICY:
            raise InvalidParamError(policy, constants.FOCUS_POLICY)
        self.setFocusPolicy(constants.FOCUS_POLICY[policy])

    def get_focus_policy(self) -> constants.FocusPolicyStr:
        """Return way the widget accepts keyboard focus.

        Returns:
            str: Focus policy
        """
        return constants.FOCUS_POLICY.inverse[self.focusPolicy()]

    def window_frame_section_at(
        self, point: datatypes.PointType
    ) -> constants.WindowFrameSectionStr:
        """Return the window frame section at given position.

        Returns:
            str: Window frame section
        """
        if isinstance(point, tuple):
            point = QtCore.QPoint(*point)
        return constants.WINDOW_FRAME_SECTION.inverse[self.windowFrameSectionAt(point)]

    def get_font(self) -> gui.Font:
        return gui.Font(self.font())

    def get_palette(self) -> gui.Palette:
        return gui.Palette(self.palette())


class GraphicsWidget(GraphicsWidgetMixin, QtWidgets.QGraphicsWidget):
    pass


if __name__ == "__main__":
    widget = GraphicsWidget()
    widget.set_layout("vertical")
