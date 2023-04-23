from __future__ import annotations

from prettyqt.qt import QtGui


class Matrix4x4(QtGui.QMatrix4x4):
    pass


if __name__ == "__main__":
    matrix = Matrix4x4([1, 2, 3, 4, 1, 2, 3, 4, 1, 2, 3, 4, 1, 2, 3, 4])
    print(matrix)
