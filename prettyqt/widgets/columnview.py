from __future__ import annotations

from prettyqt import widgets


class ColumnView(widgets.AbstractItemViewMixin, widgets.QColumnView):
    pass


if __name__ == "__main__":
    app = widgets.app()
    view = ColumnView()
    view.parent()
    view.show()
    app.exec()
