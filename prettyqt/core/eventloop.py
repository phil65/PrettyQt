from __future__ import annotations

from typing import Literal

from prettyqt import core
from prettyqt.utils import bidict


ProcessEventFlagStr = Literal[
    "all", "exclude_user_input", "exclude_socket_notifiers", "wait_for_more"
]

PROCESS_EVENT_FLAGS: bidict[ProcessEventFlagStr, core.QEventLoop.ProcessEventsFlag] = (
    bidict(
        all=core.QEventLoop.ProcessEventsFlag.AllEvents,
        exclude_user_input=core.QEventLoop.ProcessEventsFlag.ExcludeUserInputEvents,
        exclude_socket_notifiers=core.QEventLoop.ProcessEventsFlag.ExcludeSocketNotifiers,
        wait_for_more=core.QEventLoop.ProcessEventsFlag.WaitForMoreEvents,
    )
)


class EventLoop(core.ObjectMixin, core.QEventLoop):
    """Means of entering and leaving an event loop."""

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self._executing = False

    def execute(
        self,
        user_input: bool = True,
        socket_notifiers: bool = True,
        wait_for_more: bool = False,
    ) -> int:
        if self._executing:
            raise AssertionError("Eventloop is already running!")
        self._executing = True
        flag = core.QEventLoop.ProcessEventsFlag(0)
        if not user_input:
            flag |= 1
        if not socket_notifiers:
            flag |= 2
        if wait_for_more:
            flag |= 4
        status = self.exec(flag)
        self._executing = False
        return status
