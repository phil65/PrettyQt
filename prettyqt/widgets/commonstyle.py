from __future__ import annotations

from prettyqt import widgets
from prettyqt.qt import QtWidgets


class CommonStyleMixin(widgets.StyleMixin):
    pass


class CommonStyle(CommonStyleMixin, QtWidgets.QCommonStyle):
    pass


if __name__ == "__main__":
    style = CommonStyle()
