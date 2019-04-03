# -*- coding: utf-8 -*-
"""
@author: Philipp Temminghoff
"""

from qtpy import QtWidgets, QtCore


class PopupInfo(QtWidgets.QDialog):
    """
    dialog overlay to show some info to user
    """

    def __init__(self, parent=None, text=None):
        super().__init__(parent=parent)
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.close)
        self.timer.setSingleShot(True)
        self.label = QtWidgets.QLabel()
        self.setWindowFlags(self.windowFlags() |
                            QtCore.Qt.Tool |
                            QtCore.Qt.WindowStaysOnTopHint |
                            QtCore.Qt.FramelessWindowHint)
        layout = QtWidgets.QVBoxLayout()
        self.setLayout(layout)
        self.setStyleSheet("background-color: black;")  # 2a82da
        layout.addWidget(self.label)
        # signals.signals.popup_info.connect(self.popup)

    def show(self, *args, **kwargs):
        super().show(*args, **kwargs)
        screen_geo = QtWidgets.QApplication.desktop().screenGeometry()
        size = self.label.sizeHint()
        x = (screen_geo.width() - size.width()) / 2
        y = (screen_geo.height() - size.height()) / 2
        self.move(x, y - 200)
        self.timer.start(2500)

    def show_popup(self, text: str):
        self.label.setText(f"<font color='white'>{text}</font>")
        self.show()


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    widget = PopupInfo()
    widget.show_popup("test")
    app.exec_()
