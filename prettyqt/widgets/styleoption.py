from typing import TYPE_CHECKING, Self

from prettyqt.qt import QtWidgets


if TYPE_CHECKING:
    _StyleOptionBase = QtWidgets.QStyleOption
else:
    _StyleOptionBase = object


class StyleOptionMixin(_StyleOptionBase):
    @classmethod
    def based_on(cls, widget: QtWidgets.QWidget) -> Self:
        opt = cls()
        opt.initFrom(widget)
        return opt


class StyleOption(StyleOptionMixin, QtWidgets.QStyleOption):
    pass
