from typing import TYPE_CHECKING

from prettyqt import widgets


if TYPE_CHECKING:
    from prettyqt.qt import QtWidgets

    _CommonStyleBase = QtWidgets.QCommonStyle
else:
    _CommonStyleBase = object


class CommonStyleMixin(widgets.StyleMixin, _CommonStyleBase):
    pass


class CommonStyle(CommonStyleMixin, widgets.QCommonStyle):
    """Encapsulates the common Look and Feel of a GUI."""


if __name__ == "__main__":
    style = CommonStyle()
