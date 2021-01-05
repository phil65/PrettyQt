from __future__ import annotations

from prettyqt import widgets
from prettyqt.qt import QtWidgets


QtWidgets.QProxyStyle.__bases__ = (widgets.CommonStyle,)


class ProxyStyle(QtWidgets.QProxyStyle):
    pass


if __name__ == "__main__":
    style = ProxyStyle()
