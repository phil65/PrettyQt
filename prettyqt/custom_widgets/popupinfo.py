from __future__ import annotations

from prettyqt import core, iconprovider, widgets
from prettyqt.qt import QtWidgets
from prettyqt.utils import datatypes


class PopupInfo(widgets.Dialog):
    """Dialog overlay to show some info to user."""

    _singleton: PopupInfo | None = None

    def __init__(self, parent: QtWidgets.QWidget | None = None, text: str | None = None):
        super().__init__(parent=parent)
        self.timer = core.Timer(single_shot=True, timeout=self.close)
        self.label = widgets.Label(alignment="center")
        self.iconlabel = widgets.Label()
        self.set_icon("mdi.information")
        self.set_flags(stay_on_top=True, frameless=True, tooltip=True)
        layout = self.set_layout("horizontal", margin=20, size_constraint="minimum")
        self.set_background_color("black")
        self.label.set_color("white")
        layout.add(self.iconlabel)
        layout.add(self.label)
        self.hide()

    def set_text_color(self, color: datatypes.ColorType):
        self.label.set_color(color)

    def set_icon(self, icon: datatypes.IconType):
        pixmap = iconprovider.get_icon(icon, color="white").pixmap(32)
        self.iconlabel.setPixmap(pixmap)

    def show_popup(
        self,
        text: str,
        icon: datatypes.IconType = "mdi.information",
        text_color: datatypes.ColorType = "white",
        background_color: datatypes.ColorType = "black",
        position="screen",
        timeout: int = 2500,
    ):
        self.set_background_color(background_color)
        self.label.set_color(text_color)
        self.label.setText(text)
        self.set_icon(icon)
        self.adjustSize()
        self.position_on(position, y_offset=-200)
        self.timer.start(timeout)
        self.show()

    @classmethod
    def popup(
        cls,
        text: str,
        icon: datatypes.IconType = "mdi.information",
        text_color: datatypes.ColorType = "white",
        background_color: datatypes.ColorType = "black",
        position="screen",
        timeout: int = 2500,
    ):
        if cls._singleton is None:
            cls._singleton = cls()
        popup = cls._singleton
        popup.set_background_color(background_color)
        popup.label.set_color(text_color)
        popup.label.setText(text)
        popup.set_icon(icon)
        popup.adjustSize()
        popup.position_on(position, y_offset=-200)
        popup.timer.start(timeout)
        popup.show()


if __name__ == "__main__":
    app = widgets.app()
    widget = PopupInfo()
    widget.popup("2fdsfsdfsdest")
    app.sleep(1)
    widget.popup("43424234234234324")
    app.main_loop()
