from qtpy import QtCore


class PointF(QtCore.QPointF):
    def __repr__(self):
        return f"PointF(x={self.x()}, y={self.y()})"

    def __getitem__(self, index) -> float:
        return (self.x(), self.y())[index]
