from typing import Literal

from qtpy import QtCore

from prettyqt import core
from prettyqt.utils import InvalidParamError, bidict


DELETION_POLICY = bidict(
    keep=QtCore.QAbstractAnimation.KeepWhenStopped,
    delete=QtCore.QAbstractAnimation.DeleteWhenStopped,
)

DeletionPolicyStr = Literal["keep", "delete"]

DIRECTION = bidict(
    forward=QtCore.QAbstractAnimation.Forward, backward=QtCore.QAbstractAnimation.Backward
)

DirectionStr = Literal["forward", "backward"]

STATE = bidict(
    stopped=QtCore.QAbstractAnimation.Stopped,
    paused=QtCore.QAbstractAnimation.Paused,
    running=QtCore.QAbstractAnimation.Running,
)

StateStr = Literal["stopped", "paused", "running"]

QtCore.QAbstractAnimation.__bases__ = (core.Object,)


class AbstractAnimation(QtCore.QAbstractAnimation):
    def set_direction(self, direction: DirectionStr):
        """Set animation direction.

        Args:
            direction: animation direction

        Raises:
            InvalidParamError: animation direction does not exist
        """
        if direction not in DIRECTION:
            raise InvalidParamError(direction, DIRECTION)
        self.setDirection(DIRECTION[direction])

    def get_direction(self) -> DirectionStr:
        """Get the current animation direction.

        Returns:
            animation direction
        """
        return DIRECTION.inverse[self.direction()]

    def get_state(self) -> StateStr:
        """Get the current animation state.

        Returns:
            animation state
        """
        return STATE.inverse[self.state()]

    def start_animation(self, policy: DeletionPolicyStr):
        """Start the animation.

        Args:
            policy: animation policy

        Raises:
            InvalidParamError: animation policy does not exist
        """
        if policy not in DELETION_POLICY:
            raise InvalidParamError(policy, DELETION_POLICY)
        self.start(DELETION_POLICY[policy])
