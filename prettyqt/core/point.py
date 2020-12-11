from qtpy import QtCore


class Point(QtCore.QPoint):
    def __repr__(self):
        return f"Point(x={self.x()}, y={self.y()})"

    def __getitem__(self, index) -> int:
        return (self.x(), self.y())[index]
