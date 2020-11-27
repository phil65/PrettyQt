# -*- coding: utf-8 -*-

from qtpy import QtCore


class ByteArrayMatcher(QtCore.QByteArrayMatcher):
    def __repr__(self):
        return f"{type(self).__name__}({bytes(self.pattern())!r})"


if __name__ == "__main__":
    matcher = ByteArrayMatcher(b"Test")
    print(repr(matcher))
