from typing import Literal, Optional, Union

from qtpy import QtWidgets

from prettyqt import widgets
from prettyqt.utils import InvalidParamError, bidict


DIRECTION = bidict(
    left_to_right=QtWidgets.QBoxLayout.LeftToRight,
    right_to_left=QtWidgets.QBoxLayout.RightToLeft,
    top_to_bottom=QtWidgets.QBoxLayout.TopToBottom,
    bottom_to_top=QtWidgets.QBoxLayout.BottomToTop,
)

DirectionStr = Literal["left_to_right", "right_to_left", "top_to_bottom", "bottom_to_top"]


QtWidgets.QBoxLayout.__bases__ = (widgets.Layout,)


class BoxLayout(QtWidgets.QBoxLayout):
    def __init__(
        self,
        orientation="horizontal",
        parent: Optional[QtWidgets.QWidget] = None,
        margin: Optional[int] = None,
    ):
        o = self.TopToBottom if orientation == "vertical" else self.LeftToRight
        super().__init__(o, parent)
        if margin is not None:
            self.set_margin(margin)

    def serialize_fields(self):
        return dict(items=self.get_children(), direction=self.get_direction())

    def __setstate__(self, state):
        self.set_direction(state["direction"])
        for item in state["items"]:
            self.add(item)

    def __reduce__(self):
        return type(self), (), self.__getstate__()

    def __add__(self, other: Union[QtWidgets.QWidget, QtWidgets.QLayout]):
        self.add(other)
        return self

    def add(self, *item):
        for i in item:
            if isinstance(i, QtWidgets.QWidget):
                self.addWidget(i)
            else:
                self.addLayout(i)

    def add_stretch(self, stretch: int = 0):
        self.addStretch(stretch)

    def add_spacing(self, size: int):
        self.addSpacing(size)

    def set_direction(self, direction: DirectionStr):
        """Set the direction.

        Args:
            direction: direction

        Raises:
            InvalidParamError: direction does not exist
        """
        if direction not in DIRECTION:
            raise InvalidParamError(direction, DIRECTION)
        self.setDirection(DIRECTION[direction])

    def get_direction(self) -> DirectionStr:
        """Return current direction.

        Returns:
            direction
        """
        return DIRECTION.inverse[self.direction()]


if __name__ == "__main__":
    from prettyqt import widgets

    app = widgets.app()
    layout = BoxLayout("vertical")
    widget = widgets.Widget()
    widget2 = widgets.RadioButton("Test")
    layout += widget2
    widget.set_layout(layout)
    widget.show()
    app.main_loop()
