# -*- coding: utf-8 -*-

import contextlib

from qtpy import QtCore

from prettyqt import core


QtCore.QAbstractState.__bases__ = (core.Object,)


class AbstractState(QtCore.QAbstractState):
    def serialize_fields(self):
        return dict(active=self.active())

    @contextlib.contextmanager
    def on_state_active(self):
        self.onEntry()
        yield self
        self.onExit()


if __name__ == "__main__":
    state = AbstractState()
