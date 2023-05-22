from __future__ import annotations

from prettyqt import core, iconprovider, widgets
from prettyqt.qt import QtWidgets


class PopupInfo(widgets.Dialog):
    """Dialog overlay to show some info to user."""

    def __init__(self, parent: QtWidgets.QWidget | None = None, text: str | None = None):
        super().__init__(parent=parent)
        self.timer = core.Timer(single_shot=True, timeout=self.close)
        self.label = widgets.Label(alignment="center")
        self.iconlabel = widgets.Label()
        self.set_icon("mdi.information")
        self.set_flags(stay_on_top=True, frameless=True, tooltip=True)
        self.hide()
        layout = widgets.HBoxLayout(margin=20, size_constraint="minimum")
        self.set_layout(layout)
        self.set_background_color("black")
        self.label.set_color("white")
        layout.add(self.iconlabel)
        layout.add(self.label)

    def set_icon(self, icon: str):
        pixmap = iconprovider.get_icon(icon, color="white").pixmap(32)
        self.iconlabel.setPixmap(pixmap)

    def show(self):
        self.adjustSize()
        self.position_on("screen", y_offset=-200)
        super().show()
        self.timer.start(2500)

    def show_popup(self, text: str):
        self.label.setText(text)
        self.show()


if __name__ == "__main__":
    app = widgets.app()
    widget = PopupInfo()
    widget.show_popup("tfsdfdsfdsfsdfsdest")
    app.main_loop()
