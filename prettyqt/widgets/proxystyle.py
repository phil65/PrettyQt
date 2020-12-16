from qtpy import QtWidgets

from prettyqt import widgets


QtWidgets.QProxyStyle.__bases__ = (widgets.CommonStyle,)


class ProxyStyle(QtWidgets.QProxyStyle):
    pass


if __name__ == "__main__":
    style = ProxyStyle()
