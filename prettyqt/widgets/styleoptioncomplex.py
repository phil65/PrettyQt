from typing import TYPE_CHECKING

from prettyqt import widgets


if TYPE_CHECKING:
    from prettyqt.qt import QtWidgets

    _StyleOptionComplexBase = QtWidgets.QStyleOptionComplex
else:
    _StyleOptionComplexBase = object


class StyleOptionComplexMixin(widgets.StyleOptionMixin, _StyleOptionComplexBase):
    pass


class StyleOptionComplex(StyleOptionComplexMixin, widgets.QStyleOptionComplex):
    pass
