from __future__ import annotations

from prettyqt import core, gui, widgets
from prettyqt.qt import QtWidgets


class PopupInfo(widgets.Dialog):
    """Dialog overlay to show some info to user."""

    def __init__(self, parent: QtWidgets.QWidget | None = None, text: str | None = None):
        super().__init__(parent=parent)
        self.timer = core.Timer.single_shot(callback=self.close)
        self.label = widgets.Label()
        self.set_flags(stay_on_top=True, frameless=True, tool=True)
        layout = widgets.BoxLayout("vertical")
        layout.set_margin(20)
        self.set_layout(layout)
        self.set_background_color("black")
        self.label.set_color("white")
        layout.add(self.label)
        # signals.signals.popup_info.connect(self.popup)

    def show(self):
        self.hide()
        screen_geo = gui.GuiApplication.primaryScreen().geometry()
        size = self.label.sizeHint()
        x = (screen_geo.width() - size.width()) // 2
        y = (screen_geo.height() - size.height()) // 2
        self.move(x, y - 200)
        super().show()
        self.timer.start(2500)

    def show_popup(self, text: str):
        self.label.setText(text)
        self.show()


if __name__ == "__main__":
    app = widgets.app()
    widget = PopupInfo()
    widget.show_popup("test")
    app.main_loop()
