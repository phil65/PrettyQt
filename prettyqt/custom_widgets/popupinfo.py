# -*- coding: utf-8 -*-
"""
@author: Philipp Temminghoff
"""

from qtpy import QtCore, QtWidgets

from prettyqt import core, widgets


class PopupInfo(QtWidgets.QDialog):
    """
    dialog overlay to show some info to user
    """

    def __init__(self, parent=None, text=None):
        super().__init__(parent=parent)
        self.timer = core.Timer.single_shot(callback=self.close)
        self.label = widgets.Label()
        self.setWindowFlags(self.windowFlags() |
                            QtCore.Qt.Tool |
                            QtCore.Qt.WindowStaysOnTopHint |
                            QtCore.Qt.FramelessWindowHint)
        layout = widgets.BoxLayout("vertical")
        layout.set_margin(20)
        self.setLayout(layout)
        self.setStyleSheet("background-color: black;")
        self.label.setStyleSheet("color: white;")
        # self.setStyleSheet("")
        layout += self.label
        # signals.signals.popup_info.connect(self.popup)

    def show(self, *args, **kwargs):
        self.hide()
        screen_geo = widgets.Application.desktop().screenGeometry()
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
    app = widgets.Application.create_default_app()
    widget = PopupInfo()
    widget.show_popup("test")
    app.exec_()
