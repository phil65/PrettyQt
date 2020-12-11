from qtpy import QtWidgets

from prettyqt import widgets
from prettyqt.utils import bidict


SWIPE_DIRECTION = bidict(
    none=QtWidgets.QSwipeGesture.NoDirection,
    left=QtWidgets.QSwipeGesture.Left,
    right=QtWidgets.QSwipeGesture.Right,
    up=QtWidgets.QSwipeGesture.Up,
    down=QtWidgets.QSwipeGesture.Down,
)

QtWidgets.QSwipeGesture.__bases__ = (widgets.Gesture,)


class SwipeGesture(QtWidgets.QSwipeGesture):
    def get_horizontal_direction(self) -> str:
        """Return horizontal direction of the gesture.

        Possible values: "none", "left, "right"

        Returns:
            horizontal direction
        """
        return SWIPE_DIRECTION.inverse[self.horizontalDirection()]

    def get_vertical_direction(self) -> str:
        """Return vertical direction of the gesture.

        Possible values: "none", "up, "down"

        Returns:
            vertical direction
        """
        return SWIPE_DIRECTION.inverse[self.verticalDirection()]


if __name__ == "__main__":
    from prettyqt import widgets

    app = widgets.app()
    gesture = SwipeGesture()
