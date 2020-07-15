# -*- coding: utf-8 -*-
"""
"""

from qtpy import QtCore

from prettyqt import core, gui, widgets


class PopupInfo(widgets.Dialog):
    """
    dialog overlay to show some info to user
    """

    def __init__(self, parent=None, text=None):
        super().__init__(parent=parent)
        self.timer = core.Timer.single_shot(callback=self.close)
        self.label = widgets.Label()
        self.setWindowFlags(
            self.windowFlags()
            | QtCore.Qt.Tool
            | QtCore.Qt.WindowStaysOnTopHint
            | QtCore.Qt.FramelessWindowHint
        )
        layout = widgets.BoxLayout("vertical")
        layout.set_margin(20)
        self.set_layout(layout)
        self.set_background_color("black")
        self.label.set_color("white")
        layout += self.label
        # signals.signals.popup_info.connect(self.popup)

    def show(self, *args, **kwargs):
        self.hide()
        screen_geo = gui.GuiApplication.screens()[0].geometry()
        size = self.label.sizeHint()
        x = (screen_geo.width() - size.width()) / 2
        y = (screen_geo.height() - size.height()) / 2
        self.move(x, y - 200)
        super().show(*args, **kwargs)
        self.timer.start(2500)

    def show_popup(self, text: str):
        self.label.setText(text)
        self.show()


if __name__ == "__main__":
    app = widgets.app()
    widget = PopupInfo()
    widget.show_popup("test")
    app.exec_()
