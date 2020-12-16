from qtpy import QtWidgets

from prettyqt import widgets


QtWidgets.QCommonStyle.__bases__ = (widgets.Style,)


class CommonStyle(QtWidgets.QCommonStyle):
    pass


if __name__ == "__main__":
    style = CommonStyle()
