from __future__ import annotations

from typing import Literal

from prettyqt import widgets
from prettyqt.qt import QtWidgets
from prettyqt.utils import bidict


SWIPE_DIRECTION = bidict(
    none=QtWidgets.QSwipeGesture.SwipeDirection.NoDirection,
    left=QtWidgets.QSwipeGesture.SwipeDirection.Left,
    right=QtWidgets.QSwipeGesture.SwipeDirection.Right,
    up=QtWidgets.QSwipeGesture.SwipeDirection.Up,
    down=QtWidgets.QSwipeGesture.SwipeDirection.Down,
)

HorizontalDirectionStr = Literal["none", "left", "right"]
VerticalDirectionStr = Literal["none", "up", "down"]

QtWidgets.QSwipeGesture.__bases__ = (widgets.Gesture,)


class SwipeGesture(QtWidgets.QSwipeGesture):
    def get_horizontal_direction(self) -> HorizontalDirectionStr:
        """Return horizontal direction of the gesture.

        Returns:
            horizontal direction
        """
        return SWIPE_DIRECTION.inverse[self.horizontalDirection()]

    def get_vertical_direction(self) -> VerticalDirectionStr:
        """Return vertical direction of the gesture.

        Returns:
            vertical direction
        """
        return SWIPE_DIRECTION.inverse[self.verticalDirection()]


if __name__ == "__main__":
    from prettyqt import widgets

    app = widgets.app()
    gesture = SwipeGesture()
