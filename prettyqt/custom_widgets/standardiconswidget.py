from __future__ import annotations

from prettyqt import widgets
from prettyqt.qt import QtWidgets


class StandardIconsWidget(widgets.Widget):
    """Dialog showing standard icons."""

    def __init__(self, parent: QtWidgets.QWidget | None = None):
        super().__init__(parent)
        layout = widgets.HBoxLayout()
        row_nb = 14
        cindex = 0
        for k in widgets.style.STANDARD_PIXMAP:
            if cindex == 0:
                col_layout = widgets.VBoxLayout()
            icon_layout = widgets.HBoxLayout()
            icon = widgets.Application.get_style_icon(k)
            label = widgets.Label(pixmap=icon.pixmap(32, 32))
            icon_layout.addWidget(label)
            icon_layout.addWidget(widgets.LineEdit(k))
            col_layout.addLayout(icon_layout)
            cindex = (cindex + 1) % row_nb
            if cindex == 0:
                layout.addLayout(col_layout)
        self.set_layout(layout)
        self.set_title("Standard Platform Icons")
        icon = widgets.Application.get_style_icon("titlebar_menu_button")
        self.set_icon(icon)


if __name__ == "__main__":
    app = widgets.app()
    widget = StandardIconsWidget()
    widget.show()
    app.main_loop()
