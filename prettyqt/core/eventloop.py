from __future__ import annotations

from typing import Optional

from prettyqt import core
from prettyqt.qt import QtCore
from prettyqt.utils import bidict


PROCESS_EVENT_FLAGS = bidict(
    all=QtCore.QEventLoop.AllEvents,
    exclude_user_input=QtCore.QEventLoop.ExcludeUserInputEvents,
    exclude_socket_notifiers=QtCore.QEventLoop.ExcludeSocketNotifiers,
    wait_for_more=QtCore.QEventLoop.WaitForMoreEvents,
)

QtCore.QEventLoop.__bases__ = (core.Object,)


class EventLoop(QtCore.QEventLoop):
    def __init__(self, parent: Optional[QtCore.QObject] = None) -> None:
        super().__init__(parent)
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
        flag = QtCore.QEventLoop.ProcessEventFlags(0)
        if not user_input:
            flag |= 1
        if not socket_notifiers:
            flag |= 2
        if wait_for_more:
            flag |= 4
        status = self.exec_(flag)
        self._executing = False
        return status
