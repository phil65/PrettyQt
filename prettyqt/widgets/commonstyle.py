from __future__ import annotations

from prettyqt import widgets
from prettyqt.qt import QtWidgets


QtWidgets.QCommonStyle.__bases__ = (widgets.Style,)


class CommonStyle(QtWidgets.QCommonStyle):
    pass


if __name__ == "__main__":
    style = CommonStyle()
