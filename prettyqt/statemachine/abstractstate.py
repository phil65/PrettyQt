from typing import TYPE_CHECKING

from prettyqt import core
from prettyqt.qt import QtStateMachine


if TYPE_CHECKING:
    _AbstractStateBase = QtStateMachine.QAbstractState
else:
    _AbstractStateBase = object


class AbstractStateMixin(core.ObjectMixin, _AbstractStateBase):
    pass


class AbstractState(AbstractStateMixin, QtStateMachine.QAbstractState):
    pass


if __name__ == "__main__":
    state = AbstractState()
