from __future__ import annotations

from typing import Literal

from prettyqt import widgets
from prettyqt.utils import bidict


SwipeDirectionStr = Literal["none", "left", "right", "up", "down"]

SWIPE_DIRECTION: bidict[SwipeDirectionStr, widgets.QSwipeGesture.SwipeDirection] = bidict(
    none=widgets.QSwipeGesture.SwipeDirection.NoDirection,
    left=widgets.QSwipeGesture.SwipeDirection.Left,
    right=widgets.QSwipeGesture.SwipeDirection.Right,
    up=widgets.QSwipeGesture.SwipeDirection.Up,
    down=widgets.QSwipeGesture.SwipeDirection.Down,
)

HorizontalDirectionStr = Literal["none", "left", "right"]
VerticalDirectionStr = Literal["none", "up", "down"]


class SwipeGestureMixin(widgets.GestureMixin):
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


class SwipeGesture(SwipeGestureMixin, widgets.QSwipeGesture):
    pass


if __name__ == "__main__":
    from prettyqt import widgets

    app = widgets.app()
    gesture = SwipeGesture()
