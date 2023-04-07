from __future__ import annotations

from prettyqt import core
from prettyqt.qt import QtStateMachine


class AbstractStateMixin(core.ObjectMixin):
    def serialize_fields(self):
        return dict(active=self.active())


class AbstractState(AbstractStateMixin, QtStateMachine.QAbstractState):
    pass


if __name__ == "__main__":
    state = AbstractState()
