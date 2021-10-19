from __future__ import annotations

from prettyqt import core
from prettyqt.qt import QtStateMachine


QtStateMachine.QAbstractState.__bases__ = (core.Object,)


class AbstractState(QtStateMachine.QAbstractState):
    def serialize_fields(self):
        return dict(active=self.active())


if __name__ == "__main__":
    state = AbstractState()
