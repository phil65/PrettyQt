from qtpy import QtCore

from prettyqt import core
from prettyqt.utils import bidict


PROCESS_EVENT_FLAGS = bidict(
    all=QtCore.QEventLoop.AllEvents,
    exclude_user_input=QtCore.QEventLoop.ExcludeUserInputEvents,
    exclude_socket_notifiers=QtCore.QEventLoop.ExcludeSocketNotifiers,
    wait_for_more=QtCore.QEventLoop.WaitForMoreEvents,
)

QtCore.QEventLoop.__bases__ = (core.Object,)


class EventLoop(QtCore.QEventLoop):
    def execute(
        self,
        user_input: bool = True,
        socket_notifiers: bool = True,
        wait_for_more: bool = False,
    ) -> int:
        flag = 0
        if not user_input:
            flag |= 1
        if not socket_notifiers:
            flag |= 2
        if wait_for_more:
            flag |= 4
        return self.exec_(flag)
