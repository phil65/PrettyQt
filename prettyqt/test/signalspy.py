from __future__ import annotations

from prettyqt import core
from prettyqt.qt import QtTest


class SignalSpy(core.ObjectMixin, QtTest.QSignalSpy):
    pass


if __name__ == "__main__":
    from prettyqt import widgets

    app = widgets.app()
    cb = widgets.CheckBox()
    tester = SignalSpy(cb.clicked)
    cb.animateClick()
