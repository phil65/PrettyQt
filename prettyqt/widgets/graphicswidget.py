from typing import Union, Literal

from qtpy import QtWidgets, QtCore

from prettyqt import widgets, gui
from prettyqt.utils import bidict, InvalidParamError

FOCUS_POLICY = bidict(
    tab=QtCore.Qt.TabFocus,
    click=QtCore.Qt.ClickFocus,
    strong=QtCore.Qt.StrongFocus,
    wheel=QtCore.Qt.WheelFocus,
    none=QtCore.Qt.NoFocus,
)

FocusPolicyStr = Literal["tab", "click", "strong", "wheel", "none"]

QtWidgets.QGraphicsWidget.__bases__ = (widgets.GraphicsObject, widgets.GraphicsLayoutItem)


class GraphicsWidget(QtWidgets.QGraphicsWidget):
    def serialize_fields(self):
        return dict(
            autofill_background=self.autoFillBackground(),
            font=gui.Font(self.font()),
            window_title=self.windowTitle(),
            preferred_size=self.preferredSize(),
            maximum_size=self.maximumSize(),
            palette=gui.Palette(self.palette()),
            focus_policy=self.get_focus_policy(),
        )

    def set_layout(self, layout: Union[str, QtWidgets.QGraphicsLayout, None]) -> None:
        if layout is None:
            return None
        if layout == "grid":
            self.box = widgets.GraphicsGridLayout()
        elif layout in ["horizontal", "vertical"]:
            self.box = widgets.GraphicsLinearLayout(layout)
        elif layout == "anchor":
            self.box = widgets.GraphicsAnchorLayout()
        elif isinstance(layout, QtWidgets.QGraphicsLayout):
            self.box = layout
        else:
            raise ValueError("Invalid Layout")
        self.setLayout(self.box)

    def set_focus_policy(self, policy: FocusPolicyStr) -> None:
        """Set the way the widget accepts keyboard focus.

        Args:
            policy: Focus policy

        Raises:
            InvalidParamError: Description
        """
        if policy not in FOCUS_POLICY:
            raise InvalidParamError(policy, FOCUS_POLICY)
        self.setFocusPolicy(FOCUS_POLICY[policy])

    def get_focus_policy(self) -> FocusPolicyStr:
        """Return way the widget accepts keyboard focus.

        Returns:
            str: Focus policy
        """
        return FOCUS_POLICY.inverse[self.focusPolicy()]


if __name__ == "__main__":
    widget = GraphicsWidget()
    widget.set_layout("vertical")
