from qtpy import QtCore


class RectF(QtCore.QRectF):
    def __repr__(self):
        return (
            f"{type(self).__name__}({self.x()}, {self.y()}, "
            f"{self.width()}, {self.height()})"
        )

    def __reduce__(self):
        return self.__class__, (self.x(), self.y(), self.width(), self.height())


if __name__ == "__main__":
    rect = RectF(0, 2, 5, 5)
    print(repr(rect))
