from __future__ import annotations

from typing import Literal

from prettyqt import constants, core, widgets
from prettyqt.qt import QtWidgets
from prettyqt.utils import InvalidParamError, bidict


GESTURE_CANCEL_POLICY = bidict(
    none=QtWidgets.QGesture.GestureCancelPolicy.CancelNone,
    all_in_context=QtWidgets.QGesture.GestureCancelPolicy.CancelAllInContext,
)

GestureCancelPolicyStr = Literal["none", "all_in_context"]

QtWidgets.QGesture.__bases__ = (core.Object,)


class Gesture(QtWidgets.QGesture):
    def get_state(self) -> constants.GestureStateStr:
        """Return current state.

        Returns:
            state
        """
        return constants.GESTURE_STATE.inverse[self.state()]

    def get_gesture_type(self) -> constants.GestureTypeStr:
        """Return current gesture type.

        Returns:
            gesture type
        """
        return constants.GESTURE_TYPE.inverse[self.gestureType()]

    def get_hot_spot(self) -> core.PointF:
        return core.PointF(self.hotSpot())

    def set_gesture_cancel_policy(self, policy: GestureCancelPolicyStr):
        """Set gesture cancel policy.

        Args:
            policy: gesture cancel policy to use

        Raises:
            InvalidParamError: gesture cancel policy does not exist
        """
        if policy not in GESTURE_CANCEL_POLICY:
            raise InvalidParamError(policy, GESTURE_CANCEL_POLICY)
        self.setGestureCancelPolicy(GESTURE_CANCEL_POLICY[policy])

    def get_gesture_cancel_policy(self) -> GestureCancelPolicyStr:
        """Return current gesture cancel policy.

        Returns:
            gesture cancel policy
        """
        return GESTURE_CANCEL_POLICY.inverse[self.gestureCancelPolicy()]


if __name__ == "__main__":
    app = widgets.app()
    gesture = Gesture()
