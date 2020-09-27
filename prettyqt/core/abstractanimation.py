# -*- coding: utf-8 -*-

from qtpy import QtCore

from prettyqt import core
from prettyqt.utils import bidict, InvalidParamError

DELETION_POLICIES = bidict(
    keep=QtCore.QAbstractAnimation.KeepWhenStopped,
    delete=QtCore.QAbstractAnimation.DeleteWhenStopped,
)

DIRECTIONS = bidict(
    forward=QtCore.QAbstractAnimation.Forward, backward=QtCore.QAbstractAnimation.Backward
)

STATES = bidict(
    stopped=QtCore.QAbstractAnimation.Stopped,
    paused=QtCore.QAbstractAnimation.Paused,
    running=QtCore.QAbstractAnimation.Running,
)

QtCore.QAbstractAnimation.__bases__ = (core.Object,)


class AbstractAnimation(QtCore.QAbstractAnimation):
    def set_direction(self, direction: str):
        """Set animation direction.

        Valid values: "forward", "backward"

        Args:
            direction: animation direction

        Raises:
            InvalidParamError: animation direction does not exist
        """
        if direction not in DIRECTIONS:
            raise InvalidParamError(direction, DIRECTIONS)
        self.setDirection(DIRECTIONS[direction])

    def get_direction(self) -> str:
        """Get the current animation direction.

        Possible values: "forward", "backward"

        Returns:
            animation direction
        """
        return DIRECTIONS.inv[self.direction()]

    def get_state(self) -> str:
        """Get the current animation state.

        Possible values: "stopped", "paused", "running"

        Returns:
            animation state
        """
        return STATES.inv[self.state()]

    def start_animation(self, policy: str):
        """Start the animation.

        Valid values for policy: "keep", "delete"

        Args:
            policy: animation policy

        Raises:
            InvalidParamError: animation policy does not exist
        """
        if policy not in DELETION_POLICIES:
            raise InvalidParamError(policy, DELETION_POLICIES)
        self.start(DELETION_POLICIES[policy])
