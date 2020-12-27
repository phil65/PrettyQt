from prettyqt import widgets
from prettyqt.qt import QtWidgets


QtWidgets.QItemDelegate.__bases__ = (widgets.AbstractItemDelegate,)


class ItemDelegate(QtWidgets.QItemDelegate):
    pass
