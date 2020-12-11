from qtpy import QtWidgets

from prettyqt import widgets


QtWidgets.QStyleOptionRubberBand.__bases__ = (widgets.StyleOption,)


class StyleOptionRubberBand(QtWidgets.QStyleOptionRubberBand):
    pass
