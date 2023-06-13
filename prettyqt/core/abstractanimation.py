from __future__ import annotations

import functools
from typing import Literal

from prettyqt import core
from prettyqt.qt import QtCore
from prettyqt.utils import InvalidParamError, bidict


DELETION_POLICY = bidict(
    keep=QtCore.QAbstractAnimation.DeletionPolicy.KeepWhenStopped,
    delete=QtCore.QAbstractAnimation.DeletionPolicy.DeleteWhenStopped,
)

DeletionPolicyStr = Literal["keep", "delete"]

DIRECTION = bidict(
    forward=QtCore.QAbstractAnimation.Direction.Forward,
    backward=QtCore.QAbstractAnimation.Direction.Backward,
)

DirectionStr = Literal["forward", "backward"]

STATE = bidict(
    stopped=QtCore.QAbstractAnimation.State.Stopped,
    paused=QtCore.QAbstractAnimation.State.Paused,
    running=QtCore.QAbstractAnimation.State.Running,
)

StateStr = Literal["stopped", "paused", "running"]


class AbstractAnimationMixin(core.ObjectMixin):
    def __len__(self):
        return self.duration()

    def __and__(self, other: QtCore.QAbstractAnimation) -> core.SequentialAnimationGroup:
        group = core.SequentialAnimationGroup()
        group.addAnimation(self)
        group.addAnimation(other)
        return group

    def __or__(self, other: QtCore.QAbstractAnimation) -> core.ParallelAnimationGroup:
        group = core.ParallelAnimationGroup()
        group.addAnimation(self)
        group.addAnimation(other)
        return group

    def _get_map(self):
        maps = super()._get_map()
        maps |= {"direction": DIRECTION, "state": STATE}
        return maps

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

    def start_animation(
        self,
        policy: DeletionPolicyStr | core.QAbstractAnimation.DeletionPolicy = "keep",
        interval: int = 0,
        single_shot: bool = True,
    ):
        """Start the animation.

        Args:
            policy: animation policy
            interval: time interval / delay for timer
            single_shot: whether animation gets triggered once or in intervals
        """
        if policy in DELETION_POLICY.keys():
            policy = DELETION_POLICY[policy]
        if interval:
            fn = functools.partial(self.start, policy)
            self.start_callback_timer(fn, interval, single_shot=single_shot)
        else:
            self.start(policy)

    def restart_animation(self, policy: DeletionPolicyStr = "keep"):
        """Restart the animation.

        Args:
            policy: animation policy

        Raises:
            InvalidParamError: animation policy does not exist
        """
        self.stop()
        self.start_animation(policy)

    def run(self, delay: int = 0, single_shot: bool = True):
        self.start_callback_timer(self.start, delay, single_shot=single_shot)


class AbstractAnimation(AbstractAnimationMixin, QtCore.QAbstractAnimation):
    pass


if __name__ == "__main__":
    anim1 = core.PropertyAnimation()
    anim2 = core.PropertyAnimation()
    group = anim1 | anim2
    print(type(group))
