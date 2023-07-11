from __future__ import annotations

from typing import Literal

from prettyqt import constants, gui, widgets
from prettyqt.utils import datatypes


LayoutStr = Literal["grid", "horizontal", "vertical", "anchor"]


class GraphicsWidgetMixin(widgets.GraphicsObjectMixin, widgets.GraphicsLayoutItemMixin):
    @property
    def box(self):
        return self.layout()

    @box.setter
    def box(self, layout):
        self.set_layout(layout)

    def set_layout(
        self, layout: LayoutStr | widgets.QGraphicsLayout
    ) -> widgets.QGraphicsLayout:
        match layout:
            case widgets.QGraphicsLayout():
                layout = layout
            case "grid":
                layout = widgets.GraphicsGridLayout()
            case "anchor":
                layout = widgets.GraphicsAnchorLayout()
            case "horizontal" | "vertical":
                layout = widgets.GraphicsLinearLayout(layout)
            case _:
                raise ValueError(f"Invalid Layout {layout}")
        self.setLayout(layout)
        return layout

    def set_focus_policy(self, policy: constants.FocusPolicyStr | constants.FocusPolicy):
        """Set the way the widget accepts keyboard focus.

        Args:
            policy: Focus policy
        """
        self.setFocusPolicy(constants.FOCUS_POLICY.get_enum_value(policy))

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
        section = self.windowFrameSectionAt(datatypes.to_point(point))
        return constants.WINDOW_FRAME_SECTION.inverse[section]

    def get_font(self) -> gui.Font:
        return gui.Font(self.font())

    def get_palette(self) -> gui.Palette:
        return gui.Palette(self.palette())


class GraphicsWidget(GraphicsWidgetMixin, widgets.QGraphicsWidget):
    """The base class for all widget items in a QGraphicsScene."""


if __name__ == "__main__":
    widget = GraphicsWidget()
    widget.set_layout("vertical")
