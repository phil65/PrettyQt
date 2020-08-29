from typing import Union

from qtpy import QtWidgets, QtCore

from prettyqt import widgets, gui
from prettyqt.utils import bidict, InvalidParamError

FOCUS_POLICIES = bidict(
    tab=QtCore.Qt.TabFocus,
    click=QtCore.Qt.ClickFocus,
    strong=QtCore.Qt.StrongFocus,
    wheel=QtCore.Qt.WheelFocus,
    none=QtCore.Qt.NoFocus,
)

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

    def set_focus_policy(self, policy: str) -> None:
        """Set the way the widget accepts keyboard focus.

        Accepted values: "tab", "click", "strong", "wheel", "none"

        Args:
            policy (str): Focus policy

        Raises:
            InvalidParamError: Description
        """
        if policy not in FOCUS_POLICIES:
            raise InvalidParamError(policy, FOCUS_POLICIES)
        self.setFocusPolicy(FOCUS_POLICIES[policy])

    def get_focus_policy(self) -> str:
        """Return waay the widget accepts keyboard focus.

        Possible values:  "tab", "click", "strong", "wheel", "none"

        Returns:
            str: Focus policy
        """
        return FOCUS_POLICIES.inv[self.focusPolicy()]


if __name__ == "__main__":
    widget = GraphicsWidget()
    widget.set_layout("vertical")
