from qtpy import QtWidgets

from prettyqt import widgets


QtWidgets.QStyledItemDelegate.__bases__ = (widgets.AbstractItemDelegate,)


class StyledItemDelegate(QtWidgets.QStyledItemDelegate):
    pass
