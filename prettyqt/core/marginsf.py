# -*- coding: utf-8 -*-

from typing import Iterator
from qtpy import QtCore


class MarginsF(QtCore.QMarginsF):
    def __repr__(self):
        return f"MarginsF({self.left()}, {self.top()}, {self.right()}, {self.bottom()})"

    def __bool__(self):
        return not self.isNull()

    def __iter__(self) -> Iterator[float]:
        yield self.left()
        yield self.top()
        yield self.right()
        yield self.bottom()


if __name__ == "__main__":
    margins = MarginsF(0, 0, 0, 0)
    print(repr(margins))
