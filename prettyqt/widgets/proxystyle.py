from __future__ import annotations

from prettyqt import widgets
from prettyqt.qt import QtWidgets


class ProxyStyle(widgets.CommonStyleMixin, QtWidgets.QProxyStyle):
    pass


if __name__ == "__main__":
    style = ProxyStyle()
