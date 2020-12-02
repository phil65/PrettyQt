# -*- coding: utf-8 -*-

from qtpy import QtWidgets, QtCore

from prettyqt import core, widgets
from prettyqt.utils import bidict, InvalidParamError


GESTURE_TYPE = bidict(
    tap=QtCore.Qt.TapGesture,
    tap_and_hold=QtCore.Qt.TapAndHoldGesture,
    pan=QtCore.Qt.PanGesture,
    pinch=QtCore.Qt.PinchGesture,
    swipe=QtCore.Qt.SwipeGesture,
    custom=QtCore.Qt.CustomGesture,
)

GESTURE_STATE = bidict(
    none=0,  # QtCore.Qt.NoGesture,
    started=QtCore.Qt.GestureStarted,
    updated=QtCore.Qt.GestureUpdated,
    finished=QtCore.Qt.GestureFinished,
    canceled=QtCore.Qt.GestureCanceled,
)

GESTURE_CANCEL_POLICY = bidict(
    none=QtWidgets.QGesture.CancelNone,
    all_in_context=QtWidgets.QGesture.CancelAllInContext,
)

QtWidgets.QGesture.__bases__ = (core.Object,)


class Gesture(QtWidgets.QGesture):
    def get_state(self) -> str:
        """Return current state.

        Possible values: "none", "started", "updated", "finished", "canceled"

        Returns:
            state
        """
        return GESTURE_STATE.inv[self.state()]

    def get_gesture_type(self) -> str:
        """Return current gesture type.

        Possible values: "tap", "tap_and_hold", "pan", "pinch", "swipe"

        Returns:
            gesture type
        """
        return GESTURE_TYPE.inv[self.gestureType()]

    def get_hot_spot(self) -> core.PointF:
        return core.PointF(self.hotSpot())

    def set_gesture_cancel_policy(self, policy: str):
        """Set gesture cancel policy.

        Allowed values are "none", "all_in_context"

        Args:
            policy: gesture cancel policy to use

        Raises:
            InvalidParamError: gesture cancel policy does not exist
        """
        if policy not in GESTURE_CANCEL_POLICY:
            raise InvalidParamError(policy, GESTURE_CANCEL_POLICY)
        self.setGestureCancelPolicy(GESTURE_CANCEL_POLICY[policy])

    def get_gesture_cancel_policy(self) -> str:
        """Return current gesture cancel policy.

        Possible values: "none", "all_in_context"

        Returns:
            gesture cancel policy
        """
        return GESTURE_CANCEL_POLICY.inv[self.gestureCancelPolicy()]


if __name__ == "__main__":
    app = widgets.app()
    gesture = Gesture()
