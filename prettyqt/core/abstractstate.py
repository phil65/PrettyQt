from qtpy import QtCore

from prettyqt import core


QtCore.QAbstractState.__bases__ = (core.Object,)


class AbstractState(QtCore.QAbstractState):
    def serialize_fields(self):
        return dict(active=self.active())


if __name__ == "__main__":
    state = AbstractState()
