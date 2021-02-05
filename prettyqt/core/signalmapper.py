from __future__ import annotations

from prettyqt import core
from prettyqt.qt import QtCore


QtCore.QSignalMapper.__bases__ = (core.Object,)


class SignalMapper(QtCore.QSignalMapper):
    def __getitem__(self, index: int | str | QtCore.QObject) -> QtCore.QObject:
        return self.mapping(index)

    def __setitem__(self, index: QtCore.QObject, value: int | str | QtCore.QObject):
        self.setMapping(index, value)


if __name__ == "__main__":
    mapper = SignalMapper()
