# -*- coding: utf-8 -*-
"""
@author: Philipp Temminghoff
"""

import qtawesome as qta
from qtpy import QtWidgets


class PushButton(QtWidgets.QPushButton):

    def set_enabled(self):
        self.setEnabled(True)

    def set_disabled(self):
        self.setEnabled(False)

    def set_icon(self, icon):
        if isinstance(icon, str):
            icon = qta.icon(icon)
        if icon:
            self.setIcon(icon)

    def set_style_icon(self, icon):
        STYLES = dict(close=QtWidgets.QStyle.SP_TitleBarCloseButton,
                      maximise=QtWidgets.QStyle.SP_TitleBarMaxButton)
        qicon = self.style().standardIcon(STYLES[icon], None, self)
        self.setIcon(qicon)


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    widget = PushButton("This is a test")
    widget.show()
    app.exec_()
