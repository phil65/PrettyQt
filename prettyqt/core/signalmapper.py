from typing import Union

from qtpy import QtCore

from prettyqt import core


QtCore.QSignalMapper.__bases__ = (core.Object,)


class SignalMapper(QtCore.QSignalMapper):
    def __getitem__(self, index: Union[int, str, QtCore.QObject]) -> QtCore.QObject:
        return self.mapping(index)

    def __setitem__(self, index: QtCore.QObject, value: Union[int, str, QtCore.QObject]):
        self.setMapping(index, value)


if __name__ == "__main__":
    mapper = SignalMapper()
