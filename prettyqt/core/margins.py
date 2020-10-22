# -*- coding: utf-8 -*-

from qtpy import QtCore


class Margins(QtCore.QMargins):
    def __repr__(self):
        return f"Margins({self.left()}, {self.top()}, {self.right()}, {self.bottom()})"

    def __bool__(self):
        return not self.isNull()

    def __iter__(self):
        yield self.left()
        yield self.top()
        yield self.right()
        yield self.bottom()


if __name__ == "__main__":
    margins = Margins(0, 0, 0, 0)
    print(bool(margins))
