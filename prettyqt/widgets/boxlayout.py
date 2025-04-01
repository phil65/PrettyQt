from __future__ import annotations

from typing import Literal

from prettyqt import widgets
from prettyqt.utils import bidict


DirectionStr = Literal["left_to_right", "right_to_left", "top_to_bottom", "bottom_to_top"]

DIRECTION: bidict[DirectionStr, widgets.QBoxLayout.Direction] = bidict(
    left_to_right=widgets.QBoxLayout.Direction.LeftToRight,
    right_to_left=widgets.QBoxLayout.Direction.RightToLeft,
    top_to_bottom=widgets.QBoxLayout.Direction.TopToBottom,
    bottom_to_top=widgets.QBoxLayout.Direction.BottomToTop,
)


class BoxLayoutMixin(widgets.LayoutMixin):
    # def __init__(
    #     self,
    #     orientation: Literal["horizontal", "vertical"] = "horizontal",
    #     parent: widgets.QWidget | None = None,
    #     margin: int | None = None,
    # ):

    #     if margin is not None:
    #         self.set_margin(margin)

    # def __setstate__(self, state):
    #     super().__setstate__(state)
    #     self.set_direction(state["direction"])
    #     for item in state["items"]:
    #         self.add(item)

    # def __reduce__(self):
    #     return type(self), (), self.__getstate__()

    # def __add__(self, other: widgets.QWidget | widgets.QLayout):
    #     self.add(other)
    #     return self

    # def add(self, *item):
    #     for i in item:
    #         if isinstance(i, widgets.QWidget):
    #             self.addWidget(i)
    #         else:
    #             self.addLayout(i)

    def add_stretch(self, stretch: int = 0):
        self.addStretch(stretch)

    def add_spacing(self, size: int):
        self.addSpacing(size)

    def set_direction(self, direction: DirectionStr | BoxLayout.Direction):
        """Set the direction.

        Args:
            direction: direction
        """
        self.setDirection(DIRECTION.get_enum_value(direction))

    def get_direction(self) -> DirectionStr:
        """Return current direction.

        Returns:
            direction
        """
        return DIRECTION.inverse[self.direction()]


class BoxLayout(BoxLayoutMixin, widgets.QBoxLayout):
    """Lines up child widgets horizontally or vertically."""

    ID = "box"


if __name__ == "__main__":
    from prettyqt import widgets

    app = widgets.app()
    layout = widgets.VBoxLayout()
    widget = widgets.Widget()
    widget2 = widgets.RadioButton("Test")
    layout.add(widget2)
    widget.set_layout(layout)
    widget.show()
    app.exec()
