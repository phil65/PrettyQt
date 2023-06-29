from __future__ import annotations

import functools

from typing import Literal

from prettyqt import core
from prettyqt.utils import bidict


DeletionPolicyStr = Literal["keep", "delete"]

DELETION_POLICY: bidict[
    DeletionPolicyStr, core.QAbstractAnimation.DeletionPolicy
] = bidict(
    keep=core.QAbstractAnimation.DeletionPolicy.KeepWhenStopped,
    delete=core.QAbstractAnimation.DeletionPolicy.DeleteWhenStopped,
)

DirectionStr = Literal["forward", "backward"]

DIRECTION: bidict[DirectionStr, core.QAbstractAnimation.Direction] = bidict(
    forward=core.QAbstractAnimation.Direction.Forward,
    backward=core.QAbstractAnimation.Direction.Backward,
)

StateStr = Literal["stopped", "paused", "running"]

STATE: bidict[StateStr, core.QAbstractAnimation.State] = bidict(
    stopped=core.QAbstractAnimation.State.Stopped,
    paused=core.QAbstractAnimation.State.Paused,
    running=core.QAbstractAnimation.State.Running,
)


class AbstractAnimationMixin(core.ObjectMixin):
    def __len__(self):
        return self.duration()

    def __and__(self, other: core.QAbstractAnimation) -> core.SequentialAnimationGroup:
        group = core.SequentialAnimationGroup()
        group.addAnimation(self)
        group.addAnimation(other)
        return group

    def __or__(self, other: core.QAbstractAnimation) -> core.ParallelAnimationGroup:
        group = core.ParallelAnimationGroup()
        group.addAnimation(self)
        group.addAnimation(other)
        return group

    def _get_map(self):
        maps = super()._get_map()
        maps |= {"direction": DIRECTION, "state": STATE}
        return maps

    def toggle_direction(self):
        Direction = AbstractAnimation.Direction
        is_forward = self.direction() == Direction.Forward
        direction = Direction.Backward if is_forward else Direction.Forward
        self.setDirection(direction)

    def set_direction(self, direction: DirectionStr | core.QAbstractAnimation.Direction):
        """Set animation direction.

        Args:
            direction: animation direction
        """
        self.setDirection(DIRECTION.get_enum_value(direction))

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

    def restart_animation(
        self,
        policy: DeletionPolicyStr | core.QAbstractAnimation.DeletionPolicy = "keep",
    ):
        """Restart the animation.

        Args:
            policy: animation policy
        """
        self.stop()
        self.start_animation(policy)

    def run(self, delay: int = 0, single_shot: bool = True):
        self.start_callback_timer(self.start, delay, single_shot=single_shot)


class AbstractAnimation(AbstractAnimationMixin, core.QAbstractAnimation):
    pass


if __name__ == "__main__":
    anim1 = core.PropertyAnimation()
    anim2 = core.PropertyAnimation()
    group = anim1 | anim2
    print(type(group))
