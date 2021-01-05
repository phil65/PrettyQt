from __future__ import annotations

from prettyqt import widgets
from prettyqt.qt import QtWidgets


QtWidgets.QColumnView.__bases__ = (widgets.AbstractItemView,)


class ColumnView(QtWidgets.QColumnView):
    pass


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    dlg = QtWidgets.QMainWindow()
    status_bar = ColumnView()
    dlg.show()
    app.main_loop()
