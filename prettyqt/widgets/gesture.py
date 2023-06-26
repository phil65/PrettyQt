from __future__ import annotations

from typing import Literal

from prettyqt import constants, core, widgets
from prettyqt.utils import bidict


GestureCancelPolicyStr = Literal["none", "all_in_context"]

GESTURE_CANCEL_POLICY: bidict[
    GestureCancelPolicyStr, widgets.QGesture.GestureCancelPolicy
] = bidict(
    none=widgets.QGesture.GestureCancelPolicy.CancelNone,
    all_in_context=widgets.QGesture.GestureCancelPolicy.CancelAllInContext,
)


class GestureMixin(core.ObjectMixin):
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

    def set_gesture_cancel_policy(
        self, policy: GestureCancelPolicyStr | widgets.QGesture.GestureCancelPolicy
    ):
        """Set gesture cancel policy.

        Args:
            policy: gesture cancel policy to use
        """
        self.setGestureCancelPolicy(GESTURE_CANCEL_POLICY.get_enum_value(policy))

    def get_gesture_cancel_policy(self) -> GestureCancelPolicyStr:
        """Return current gesture cancel policy.

        Returns:
            gesture cancel policy
        """
        return GESTURE_CANCEL_POLICY.inverse[self.gestureCancelPolicy()]


class Gesture(GestureMixin, widgets.QGesture):
    pass


if __name__ == "__main__":
    app = widgets.app()
    gesture = Gesture()
