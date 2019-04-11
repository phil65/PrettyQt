# -*- coding: utf-8 -*-
"""
@author: Philipp Temminghoff
"""

from qtpy import QtCore, QtWidgets

from prettyqt import widgets, core


class PopupInfo(QtWidgets.QDialog):
    """
    dialog overlay to show some info to user
    """

    def __init__(self, parent=None, text=None):
        super().__init__(parent=parent)
        self.timer = core.Timer()
        self.timer.timeout.connect(self.close)
        self.timer.setSingleShot(True)
        self.label = widgets.Label()
        self.setWindowFlags(self.windowFlags() |
                            QtCore.Qt.Tool |
                            QtCore.Qt.WindowStaysOnTopHint |
                            QtCore.Qt.FramelessWindowHint)
        layout = widgets.BoxLayout("vertical")
        self.setLayout(layout)
        self.setStyleSheet("background-color: black;")  # 2a82da
        layout.addWidget(self.label)
        # signals.signals.popup_info.connect(self.popup)

    def show(self, *args, **kwargs):
        super().show(*args, **kwargs)
        screen_geo = widgets.Application.desktop().screenGeometry()
        size = self.label.sizeHint()
        x = (screen_geo.width() - size.width()) / 2
        y = (screen_geo.height() - size.height()) / 2
        self.move(x, y - 200)
        self.timer.start(2500)

    def show_popup(self, text: str):
        self.label.setText(f"<font color='white'>{text}</font>")
        self.show()


if __name__ == "__main__":
    app = widgets.Application.create_default_app()
    widget = PopupInfo()
    widget.show_popup("test")
    app.exec_()
