from qtpy import QtCore


class ByteArrayMatcher(QtCore.QByteArrayMatcher):
    def __repr__(self):
        return f"{type(self).__name__}({self.get_pattern()!r})"

    def get_pattern(self) -> bytes:
        return bytes(self.pattern())


if __name__ == "__main__":
    matcher = ByteArrayMatcher(b"Test")
