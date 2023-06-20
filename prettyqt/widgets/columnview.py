from __future__ import annotations

from prettyqt import widgets
from prettyqt.qt import QtWidgets


class ColumnView(widgets.AbstractItemViewMixin, QtWidgets.QColumnView):
    pass


if __name__ == "__main__":
    app = widgets.app()
    view = ColumnView()
    view.parent()
    view.show()
    app.main_loop()
