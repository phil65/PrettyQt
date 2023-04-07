from __future__ import annotations

from prettyqt import widgets
from prettyqt.qt import QtWidgets


class StyleOptionComplexMixin(widgets.StyleOptionMixin):
    pass


class StyleOptionComplex(StyleOptionComplexMixin, QtWidgets.QStyleOptionComplex):
    pass
