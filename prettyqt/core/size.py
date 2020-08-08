# -*- coding: utf-8 -*-

from qtpy import QtCore


class Size(QtCore.QSize):
    def __repr__(self):
        return f"Size({self.width()}, {self.height()})"

    def __getitem__(self, index) -> int:
        return (self.width(), self.height())[index]

    def __reduce__(self):
        return (self.__class__, (self.width(), self.height()))


if __name__ == "__main__":
    size = Size(10, 20)
    print(tuple(size))
