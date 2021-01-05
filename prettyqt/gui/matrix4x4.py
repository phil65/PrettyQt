from __future__ import annotations

from prettyqt.qt import QtGui


class Matrix4x4(QtGui.QMatrix4x4):
    # def __repr__(self):
    #     return f"{type(self).__name__}()"
    pass


if __name__ == "__main__":
    matrix = Matrix4x4([1, 2, 3, 4, 1, 2, 3, 4, 1, 2, 3, 4, 1, 2, 3, 4])
    print(matrix)
